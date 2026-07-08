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
from langchain_core.messages import HumanMessage, SystemMessage

from janseva.agents.llm import get_llm
from janseva.db.engine import async_session_factory
from janseva.db.models.anonymous_report import AnonymousReport
from janseva.reporting.anonymizer import strip_metadata
from janseva.reporting.encryption import encrypt_content
from janseva.reporting.router import determine_routing
from janseva.reporting.tokens import generate_report_token

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
    system_msg = SystemMessage(
        content=REPORT_SYSTEM_PROMPT.format(
            user_language=user_language,
        )
    )

    structuring_prompt = HumanMessage(
        content=f"""
The user wants to submit an anonymous report. Their message is:
"{latest_message}"

Please:
1. Acknowledge their report
2. Summarize what they reported in a clear, structured format
3. Explain that their identity is fully protected
4. Provide their anonymous tracking token (will be inserted below)
"""
    )

    # Step 2: Anonymize the content
    anonymized_text = strip_metadata(latest_message)

    if not anonymized_text or len(anonymized_text.strip()) < 10:
        return {
            "response": "कृपया अपनी शिकायत का विवरण थोड़ा और विस्तार से दें ताकि हम उचित कार्रवाई कर सकें।\n"
                        "Please provide a bit more detail about your complaint so we can take appropriate action."
        }

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
            severity=routing.get("severity", "medium"),
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
