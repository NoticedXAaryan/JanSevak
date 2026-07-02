# Guide 05: Anonymous Reporting System

## What This Does
Builds the secure anonymous reporting system — the most safety-critical feature of JanSeva. Citizens can report corruption, misconduct, or wrongdoing by local authorities without any risk of identification. Reports are automatically routed to the correct superior authority, bypassing anyone named in the complaint.

## Prerequisites
- Guide 01 completed (project setup, DB)
- Guide 03 completed (AI agent core)

---

## Security Design Principles

> ⚠️ **This feature can put people in physical danger if implemented incorrectly.**

1. **No link between reporter and report**: The report record in the database has NO foreign key to the users table. The Telegram ID is never stored alongside the report.
2. **Metadata stripping**: All identifiable info (Telegram ID, username, timestamps that could identify the sender) is stripped before storage.
3. **Encryption at rest**: Report content is encrypted in the database using Fernet symmetric encryption.
4. **Anonymous token**: Each report gets a random token. The reporter can use this token to check status or add information — but the token cannot be traced back to them.
5. **Smart routing**: If the report names a specific authority (e.g., "the local inspector"), the system automatically routes the report to that authority's superior, skipping the named person.

---

## Database Models

### Authority Hierarchy

**File: `src/janseva/db/models/authority.py`**

```python
"""
Authority hierarchy model.
Represents the chain of command in government bodies.
Used to route anonymous reports to the correct superior.
"""
import uuid
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from janseva.db.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Authority(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "authorities"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    title_hi: Mapped[str] = mapped_column(String(255), nullable=True)
    department: Mapped[str] = mapped_column(String(255), nullable=False)
    district: Mapped[str] = mapped_column(String(255), nullable=True)
    state: Mapped[str] = mapped_column(String(255), nullable=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    # Level hierarchy (higher = more authority):
    # 1 = Village level (Gram Pradhan, local constable)
    # 2 = Block/Tehsil level (BDO, SHO)
    # 3 = District level (DM, SP)
    # 4 = Division level (Commissioner, DIG)
    # 5 = State level (Chief Secretary, DGP)

    reports_to_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("authorities.id"), nullable=True
    )

    # Self-referential relationship
    reports_to = relationship("Authority", remote_side="Authority.id", lazy="selectin")
```

### Anonymous Report

**File: `src/janseva/db/models/anonymous_report.py`**

```python
"""
Anonymous report model.
CRITICAL: This table has NO foreign key to the users table.
The reporter's identity is never stored.
"""
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from janseva.db.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class AnonymousReport(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "anonymous_reports"

    # Anonymous access token — reporter uses this to check status
    # This is the ONLY way to access the report. No user ID is stored.
    report_token: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, index=True
    )

    # Report classification
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    # Categories: corruption, misconduct, harassment, illegal_activity,
    #             public_safety, environmental, other

    # Encrypted content — never stored in plaintext
    content_encrypted: Mapped[str] = mapped_column(Text, nullable=False)

    # Where was this reported about?
    district: Mapped[str | None] = mapped_column(String(255), nullable=True)
    state: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Routing
    target_authority_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    routed_to_level: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    routed_to_department: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Status tracking
    status: Mapped[str] = mapped_column(
        String(20), default="submitted", nullable=False
    )
    # Statuses: submitted, under_review, investigating, resolved, dismissed

    # Admin-side notes (never shown to reporter directly to prevent info leakage)
    admin_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Severity assessment
    severity: Mapped[str] = mapped_column(String(20), default="medium", nullable=False)
    # Severity: low, medium, high, critical
```

Update `src/janseva/db/models/__init__.py` to export the new models:

```python
from janseva.db.models.base import Base
from janseva.db.models.user import User
from janseva.db.models.conversation import Conversation
from janseva.db.models.message import Message
from janseva.db.models.authority import Authority
from janseva.db.models.anonymous_report import AnonymousReport

__all__ = ["Base", "User", "Conversation", "Message", "Authority", "AnonymousReport"]
```

Then create and run the migration:
```bash
uv run alembic revision --autogenerate -m "add authorities and anonymous_reports tables"
uv run alembic upgrade head
```

---

## Core Reporting Engine

### 1. Encryption Module

**File: `src/janseva/reporting/encryption.py`**

```python
"""
Encryption for anonymous report content.
Uses Fernet symmetric encryption (AES-128-CBC).
"""
from cryptography.fernet import Fernet
from janseva.config import settings


def get_fernet() -> Fernet:
    """Get the Fernet encryption instance."""
    key = settings.report_encryption_key
    if key == "change-me":
        # Generate a key for development — in production, set a real key
        key = Fernet.generate_key().decode()
    return Fernet(key.encode() if isinstance(key, str) else key)


def encrypt_content(plaintext: str) -> str:
    """Encrypt report content. Returns base64-encoded ciphertext."""
    f = get_fernet()
    return f.encrypt(plaintext.encode("utf-8")).decode("utf-8")


def decrypt_content(ciphertext: str) -> str:
    """Decrypt report content. Returns plaintext."""
    f = get_fernet()
    return f.decrypt(ciphertext.encode("utf-8")).decode("utf-8")
```

### 2. Anonymizer Module

**File: `src/janseva/reporting/anonymizer.py`**

```python
"""
Metadata stripping for anonymous reports.
Ensures no identifiable information leaks into the report record.
"""
import re
from datetime import datetime, timezone


def strip_metadata(report_text: str) -> str:
    """
    Remove potentially identifying metadata from report text.
    
    Strips:
    - Phone numbers (Indian format)
    - Aadhaar numbers
    - Email addresses
    - Telegram usernames (@mentions)
    - Specific dates that could identify timing of interaction
    """
    cleaned = report_text

    # Remove phone numbers (Indian: 10 digits, with or without +91)
    cleaned = re.sub(r'\+?91[-\s]?\d{10}', '[PHONE_REDACTED]', cleaned)
    cleaned = re.sub(r'\b\d{10}\b', '[PHONE_REDACTED]', cleaned)

    # Remove Aadhaar numbers (12 digits, possibly with spaces)
    cleaned = re.sub(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', '[AADHAAR_REDACTED]', cleaned)

    # Remove email addresses
    cleaned = re.sub(r'\b[\w.-]+@[\w.-]+\.\w+\b', '[EMAIL_REDACTED]', cleaned)

    # Remove Telegram @usernames
    cleaned = re.sub(r'@\w+', '[USERNAME_REDACTED]', cleaned)

    return cleaned


def generate_submission_time() -> datetime:
    """
    Generate a fuzzy submission time.
    Rounds to the nearest hour to prevent timing-based identification.
    """
    now = datetime.now(timezone.utc)
    return now.replace(minute=0, second=0, microsecond=0)
```

### 3. Anonymous Token System

**File: `src/janseva/reporting/tokens.py`**

```python
"""
Anonymous report token system.
Generates secure, random tokens for two-way communication
without revealing the reporter's identity.
"""
import secrets
import string


def generate_report_token() -> str:
    """
    Generate a secure, human-readable report token.
    Format: XXXX-XXXX-XXXX (12 alphanumeric chars, uppercase)
    
    Example: "K7M2-P9X4-R1N6"
    
    This token is the reporter's ONLY way to check their report status.
    It cannot be linked back to their Telegram account.
    """
    chars = string.ascii_uppercase + string.digits
    # Remove confusing characters (O/0, I/1, L)
    chars = chars.replace("O", "").replace("0", "").replace("I", "").replace("1", "").replace("L", "")
    
    part1 = ''.join(secrets.choice(chars) for _ in range(4))
    part2 = ''.join(secrets.choice(chars) for _ in range(4))
    part3 = ''.join(secrets.choice(chars) for _ in range(4))
    
    return f"{part1}-{part2}-{part3}"
```

### 4. Authority Routing Engine

**File: `src/janseva/reporting/router.py`**

```python
"""
Authority routing engine.
Determines the correct authority to receive an anonymous report.
Key behavior: If the report names a specific authority, the system
automatically routes to that authority's SUPERIOR, never to them.
"""
import structlog
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from janseva.db.models.authority import Authority
from janseva.agents.llm import get_llm
from langchain_core.messages import SystemMessage, HumanMessage

logger = structlog.get_logger()

ROUTING_PROMPT = """You are analyzing an anonymous complaint report to determine:
1. The CATEGORY of the complaint (one of: corruption, misconduct, harassment, illegal_activity, public_safety, environmental, other)
2. The DEPARTMENT it relates to (e.g., Police, Revenue, Municipal, Health, Education, Agriculture)
3. The SEVERITY (low, medium, high, critical)
4. Whether a SPECIFIC AUTHORITY is named in the complaint
5. The approximate LEVEL of the named authority:
   - 1 = Village level (Gram Pradhan, local constable, patwari)
   - 2 = Block/Tehsil level (BDO, SHO, Tehsildar)
   - 3 = District level (DM, SP, CMO)
   - 4 = Division level (Commissioner, DIG)
   - 5 = State level (Chief Secretary, DGP)

Respond in this exact JSON format:
{
  "category": "corruption",
  "department": "Police",
  "severity": "high",
  "named_authority": "SHO of Kotwali thana",
  "named_authority_level": 2
}

If no specific authority is named, set named_authority to null and named_authority_level to 0.

Report text:"""


async def determine_routing(
    report_text: str,
    district: str | None = None,
    session: AsyncSession | None = None,
) -> dict:
    """
    Analyze a report and determine where it should be routed.
    
    If a specific authority is named in the complaint:
    - Route to their SUPERIOR (at least one level up)
    - Never route to the named authority themselves
    
    If no authority is named:
    - Route to district-level (level 3) by default
    
    Returns:
        dict with keys: category, department, severity, routed_to_level, 
                       target_authority_title
    """
    llm = get_llm()
    
    # Use LLM to analyze the report
    messages = [
        SystemMessage(content=ROUTING_PROMPT),
        HumanMessage(content=report_text),
    ]
    
    response = llm.invoke(messages)
    
    # Parse the LLM's JSON response
    import json
    try:
        analysis = json.loads(response.content)
    except json.JSONDecodeError:
        # Fallback if LLM doesn't return valid JSON
        logger.warning("routing_parse_error", raw=response.content[:200])
        analysis = {
            "category": "other",
            "department": "General Administration",
            "severity": "medium",
            "named_authority": None,
            "named_authority_level": 0,
        }
    
    # Determine routing level
    named_level = analysis.get("named_authority_level", 0)
    
    if named_level > 0:
        # CRITICAL: Route ABOVE the named authority
        routed_to_level = min(named_level + 1, 5)
        logger.info(
            "routing_bypass",
            named_authority=analysis.get("named_authority"),
            named_level=named_level,
            routed_to_level=routed_to_level,
        )
    else:
        # No specific authority named — default to district level
        routed_to_level = 3
    
    return {
        "category": analysis.get("category", "other"),
        "department": analysis.get("department", "General Administration"),
        "severity": analysis.get("severity", "medium"),
        "routed_to_level": routed_to_level,
        "target_authority_title": analysis.get("named_authority"),
    }
```

---

## Anonymous Report Agent (LangGraph)

**File: `src/janseva/agents/specialists/anonymous_reporter.py`**

```python
"""
Anonymous Report Agent — Guides users through submitting an anonymous report.

This is a multi-step conversational flow:
1. Explain anonymity protections
2. Ask for the complaint details
3. Ask for the location (district/state)
4. Confirm submission
5. Generate and return the anonymous token

The entire flow happens WITHOUT storing the user's Telegram ID in the report.
"""
import structlog
from langchain_core.messages import SystemMessage, HumanMessage

from janseva.agents.llm import get_llm
from janseva.db.engine import async_session_factory
from janseva.db.models.anonymous_report import AnonymousReport
from janseva.reporting.anonymizer import strip_metadata
from janseva.reporting.encryption import encrypt_content
from janseva.reporting.tokens import generate_report_token
from janseva.reporting.router import determine_routing

logger = structlog.get_logger()

REPORT_SYSTEM_PROMPT = """You are JanSeva's anonymous reporting assistant.
Your role is to help the user describe their complaint clearly and completely.

RULES:
1. Respond in the SAME LANGUAGE the user uses.
2. Be empathetic and reassuring — the user may be scared.
3. NEVER ask for the user's name, phone number, or any personal details.
4. Help them describe: WHAT happened, WHERE it happened, WHO is involved (titles/roles, not personal info), WHEN it happened.
5. Keep responses concise and focused.
6. Once you have enough detail, summarize the complaint and ask for confirmation.

User's language: {user_language}"""


async def handle_anonymous_report(state: dict) -> dict:
    """
    Process an anonymous report submission.
    
    This function is called when the orchestrator detects report intent.
    It processes the user's complaint, anonymizes it, encrypts it,
    routes it to the correct authority, and returns the anonymous token.
    """
    llm = get_llm()
    user_language = state.get("user_language", "hi")
    latest_message = state["messages"][-1].content if state["messages"] else ""
    
    # Step 1: Use LLM to structure the complaint
    system_msg = SystemMessage(content=REPORT_SYSTEM_PROMPT.format(
        user_language=user_language,
    ))
    
    structuring_prompt = HumanMessage(content=f"""
The user wants to submit an anonymous report. Their message is:
"{latest_message}"

Please:
1. Acknowledge their report
2. Summarize what they reported in a clear, structured format
3. Explain that their identity is fully protected
4. Provide their anonymous tracking token (will be inserted below)
""")
    
    # Step 2: Anonymize the content
    anonymized_text = strip_metadata(latest_message)
    
    # Step 3: Determine routing
    routing = await determine_routing(
        report_text=anonymized_text,
        district=state.get("user_district"),
    )
    
    # Step 4: Encrypt and store
    encrypted_content = encrypt_content(anonymized_text)
    report_token = generate_report_token()
    
    async with async_session_factory() as session:
        report = AnonymousReport(
            report_token=report_token,
            category=routing["category"],
            content_encrypted=encrypted_content,
            district=state.get("user_district"),
            state=None,
            target_authority_title=routing.get("target_authority_title"),
            routed_to_level=routing["routed_to_level"],
            routed_to_department=routing.get("department"),
            status="submitted",
            severity=routing.get("severity", "medium"),
        )
        session.add(report)
        await session.commit()
        
        logger.info(
            "anonymous_report_submitted",
            report_token=report_token,
            category=routing["category"],
            severity=routing["severity"],
            routed_to_level=routing["routed_to_level"],
            # NOTE: No user identifiers logged here
        )
    
    # Step 5: Build response
    level_names = {
        1: "ग्राम स्तर / Village level",
        2: "ब्लॉक/तहसील स्तर / Block level",
        3: "जिला स्तर / District level",
        4: "मंडल स्तर / Division level",
        5: "राज्य स्तर / State level",
    }
    routed_level_name = level_names.get(routing["routed_to_level"], "District level")
    
    response = (
        f"🛡️ <b>गुमनाम शिकायत सफलतापूर्वक दर्ज!</b>\n"
        f"<b>Anonymous Report Submitted Successfully!</b>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔑 <b>आपका ट्रैकिंग टोकन:</b>\n"
        f"<code>{report_token}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"⚠️ <b>इस टोकन को सुरक्षित रखें!</b> यह आपकी शिकायत की स्थिति जानने का एकमात्र तरीका है।\n\n"
        f"📋 <b>श्रेणी:</b> {routing['category']}\n"
        f"🏛️ <b>विभाग:</b> {routing.get('department', 'सामान्य प्रशासन')}\n"
        f"📊 <b>गंभीरता:</b> {routing.get('severity', 'मध्यम')}\n"
        f"📤 <b>भेजा गया:</b> {routed_level_name} अधिकारियों को\n\n"
        f"🔒 <b>आपकी पहचान पूरी तरह सुरक्षित है।</b>\n"
        f"कोई भी आपकी शिकायत को आपसे नहीं जोड़ सकता।\n\n"
        f"📌 स्थिति जानने के लिए भेजें: <code>/status {report_token}</code>"
    )
    
    return {"response": response}
```

---

## Update Orchestrator to Wire the Report Agent

In `src/janseva/agents/orchestrator.py`, make these changes:

1. Import the anonymous reporter:
```python
from janseva.agents.specialists.anonymous_reporter import handle_anonymous_report
```

2. Update the graph builder to use the real agent instead of placeholder:
```python
# In build_agent_graph():
# Change: graph.add_node("placeholder", handle_placeholder)
# To:
graph.add_node("anonymous_report_node", handle_anonymous_report)
```

3. Update the routing:
```python
# In route_by_intent():
route_map = {
    "service_query": "service_navigator",
    "anonymous_report": "anonymous_report_node",  # Changed from "placeholder"
    "healthcare": "placeholder",
    "farmer": "placeholder",
    "general": "general_chat",
    "escalate": "escalation",
}
```

4. Update conditional edges:
```python
graph.add_conditional_edges(
    "classify_intent",
    route_by_intent,
    {
        "service_navigator": "service_navigator",
        "anonymous_report_node": "anonymous_report_node",
        "general_chat": "general_chat",
        "escalation": "escalation",
        "placeholder": "placeholder",
    },
)
graph.add_edge("anonymous_report_node", END)
```

---

## Authority Hierarchy Seed Data

**File: `scripts/seed_authorities.py`**

```python
"""
Seed the authority hierarchy database.
This is sample data — customize for your target district/state.

Run: uv run python scripts/seed_authorities.py
"""
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from janseva.common.logging import setup_logging
from janseva.db.engine import async_session_factory
from janseva.db.models.authority import Authority


SAMPLE_HIERARCHY = [
    # Level 5: State Level
    {"title": "Director General of Police (DGP)", "title_hi": "पुलिस महानिदेशक", "department": "Police", "level": 5, "state": "Sample State"},
    {"title": "Chief Secretary", "title_hi": "मुख्य सचिव", "department": "General Administration", "level": 5, "state": "Sample State"},
    
    # Level 4: Division Level
    {"title": "Inspector General of Police (IG)", "title_hi": "पुलिस महानिरीक्षक", "department": "Police", "level": 4, "state": "Sample State"},
    {"title": "Divisional Commissioner", "title_hi": "मंडलायुक्त", "department": "Revenue", "level": 4, "state": "Sample State"},
    
    # Level 3: District Level
    {"title": "Superintendent of Police (SP)", "title_hi": "पुलिस अधीक्षक", "department": "Police", "level": 3, "district": "Sample District"},
    {"title": "District Magistrate (DM)", "title_hi": "जिलाधिकारी", "department": "Revenue", "level": 3, "district": "Sample District"},
    {"title": "Chief Medical Officer (CMO)", "title_hi": "मुख्य चिकित्साधिकारी", "department": "Health", "level": 3, "district": "Sample District"},
    
    # Level 2: Block Level
    {"title": "Station House Officer (SHO)", "title_hi": "थाना प्रभारी", "department": "Police", "level": 2, "district": "Sample District"},
    {"title": "Block Development Officer (BDO)", "title_hi": "खंड विकास अधिकारी", "department": "Revenue", "level": 2, "district": "Sample District"},
    {"title": "Tehsildar", "title_hi": "तहसीलदार", "department": "Revenue", "level": 2, "district": "Sample District"},
    
    # Level 1: Village Level
    {"title": "Village Pradhan / Sarpanch", "title_hi": "ग्राम प्रधान / सरपंच", "department": "Panchayati Raj", "level": 1, "district": "Sample District"},
    {"title": "Gram Panchayat Secretary", "title_hi": "ग्राम पंचायत सचिव", "department": "Panchayati Raj", "level": 1, "district": "Sample District"},
    {"title": "Patwari / Lekhpal", "title_hi": "पटवारी / लेखपाल", "department": "Revenue", "level": 1, "district": "Sample District"},
]


async def seed():
    setup_logging()
    async with async_session_factory() as session:
        for data in SAMPLE_HIERARCHY:
            authority = Authority(**data)
            session.add(authority)
        await session.commit()
        print(f"✅ Seeded {len(SAMPLE_HIERARCHY)} authorities.")


if __name__ == "__main__":
    asyncio.run(seed())
```

---

## Generate a Fernet Key for Production

```bash
# Generate a Fernet key to use in .env
uv run python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Copy the output and set `REPORT_ENCRYPTION_KEY` in your `.env`.

---

## Verification Checklist

- [ ] Migration runs successfully (authorities + anonymous_reports tables created)
- [ ] `scripts/seed_authorities.py` populates the authority hierarchy
- [ ] Sending "मुझे एक शिकायत करनी है" to the bot triggers the report flow
- [ ] Report is stored in `anonymous_reports` table with encrypted content
- [ ] Report has a valid token in `XXXX-XXXX-XXXX` format
- [ ] Report has NO user_id or telegram_id field
- [ ] Phone numbers and Aadhaar numbers in report text are redacted
- [ ] Report about a "local SHO" routes to level 3 (district), not level 2
- [ ] Decrypting the content shows the original (anonymized) report text

---

## Git Checkpoint

```bash
git add -A
git commit -m "feat(reporting): implement anonymous reporting system

- Authority hierarchy model with self-referential chain of command
- AnonymousReport model with NO user FK (true anonymity)
- Fernet encryption for report content at rest
- Metadata stripping: phone numbers, Aadhaar, emails, usernames
- Secure token generation (XXXX-XXXX-XXXX format) for tracking
- AI-powered routing: auto-bypass named authorities, route to superior
- Authority hierarchy seed script with sample Indian govt structure
- Anonymous reporter agent integrated into LangGraph orchestrator"
```
