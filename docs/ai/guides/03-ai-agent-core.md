# Guide 03: AI Agent Core (LangGraph)

## What This Does
Builds the AI brain of JanSeva using LangGraph. This creates:
1. **Orchestrator Agent** — Classifies user intent and routes to the correct specialist
2. **Service Navigator Agent** — Answers "what do I need for X?" questions about government services
3. **Conversation Memory** — Persists chat history so the AI remembers context across messages
4. Wires everything to the Telegram bot so real conversations flow through the AI

## Prerequisites
- Guide 01 completed (project setup, DB running)
- Guide 02 completed (Telegram bot working with echo)
- LLM access configured in `.env`:
  - **Option A (Recommended)**: `GOOGLE_API_KEY` set + `LLM_PROVIDER=gemini`
  - **Option B (Free/Local)**: Ollama installed + running + `LLM_PROVIDER=ollama`

---

## Concept: How LangGraph Works

LangGraph models AI workflows as **directed graphs**:

```
User Message
    │
    ▼
┌─────────────┐
│ Orchestrator │ ← Classifies intent: "service_query", "anonymous_report",
│   (Node 1)   │   "healthcare", "farmer", "general", "escalate"
└──────┬──────┘
       │ (conditional edge based on intent)
       ├── intent == "service_query" ──► Service Navigator Agent ──► Response
       ├── intent == "anonymous_report" ──► Anonymous Report Agent ──► Response
       ├── intent == "healthcare" ──► Healthcare Agent ──► Response
       ├── intent == "farmer" ──► Farmer Agent ──► Response
       ├── intent == "general" ──► General Chat (LLM direct) ──► Response
       └── intent == "escalate" ──► Escalation Agent ──► Response
```

**State** flows through the graph. Each node reads state, does work, and updates state. The final state contains the response to send back to the user.

---

## Files to Create

### 1. LangGraph State Definition

**File: `src/janseva/agents/state.py`**

```python
"""
LangGraph state definitions.
State is the data that flows through the agent graph.
Every node reads and updates this shared state.
"""
from __future__ import annotations

from typing import Annotated, Literal, Sequence
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    Shared state for the JanSeva agent graph.
    
    Fields:
        messages: Full conversation history (LangChain message format).
                  Uses `add_messages` reducer to append, not replace.
        user_language: Detected language of the user (e.g., 'hi', 'en', 'mr').
        user_district: User's district/location for localized results.
        user_telegram_id: Telegram user ID for DB lookups.
        intent: Classified intent from the orchestrator.
        response: Final text response to send back to the user.
        needs_escalation: Whether the query should be escalated to admin.
        escalation_reason: Why the query was escalated.
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]
    user_language: str
    user_district: str
    user_telegram_id: int
    intent: str
    response: str
    needs_escalation: bool
    escalation_reason: str
```

---

### 2. LLM Provider Setup

**File: `src/janseva/agents/llm.py`**

```python
"""
LLM provider factory.
Returns the configured LLM instance based on settings.
Supports Google Gemini (production) and Ollama (local development).
"""
from langchain_core.language_models import BaseChatModel
from janseva.config import settings


def get_llm() -> BaseChatModel:
    """
    Create and return the configured LLM instance.
    
    Uses LLM_PROVIDER from settings:
    - 'gemini': Google Gemini API (requires GOOGLE_API_KEY)
    - 'ollama': Local Ollama instance (requires Ollama running)
    """
    if settings.llm_provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        return ChatGoogleGenerativeAI(
            model=settings.llm_model,
            google_api_key=settings.google_api_key,
            temperature=0.3,  # Low temperature for factual government info
            max_output_tokens=2048,
        )
    elif settings.llm_provider == "ollama":
        from langchain_community.chat_models import ChatOllama
        
        return ChatOllama(
            model=settings.llm_model,
            base_url=settings.ollama_base_url,
            temperature=0.3,
        )
    else:
        raise ValueError(
            f"Unknown LLM provider: {settings.llm_provider}. "
            "Set LLM_PROVIDER to 'gemini' or 'ollama' in .env"
        )
```

---

### 3. Orchestrator Agent (Intent Classifier)

**File: `src/janseva/agents/orchestrator.py`**

```python
"""
Orchestrator Agent — The brain of JanSeva.

This is the main LangGraph graph. It:
1. Classifies user intent (what kind of question is this?)
2. Routes to the appropriate specialist agent
3. Returns the final response

The graph looks like:
    classify_intent → route_to_specialist → [specialist_node] → format_response
"""
import structlog
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

from janseva.agents.state import AgentState
from janseva.agents.llm import get_llm
from janseva.agents.specialists.service_navigator import handle_service_query
from janseva.agents.specialists.escalation import handle_escalation

logger = structlog.get_logger()

# --- System Prompts ---

INTENT_CLASSIFIER_PROMPT = """You are JanSeva (जनसेवा), an AI assistant that helps Indian citizens interact with government services.

Your job is to classify the user's message into one of these intents:

1. "service_query" — Questions about government services, documents, certificates, requirements, applications, forms
   Examples: "आय प्रमाण पत्र कैसे बनाएं?", "What documents for caste certificate?", "land record kaise dekhe?"

2. "anonymous_report" — User wants to report corruption, misconduct, or wrongdoing anonymously
   Examples: "मुझे एक शिकायत दर्ज करनी है", "I want to report a corrupt officer", "hamare area mein galat kaam ho raha hai"

3. "healthcare" — Questions about hospitals, doctors, appointments, medical facilities
   Examples: "नजदीकी अस्पताल कौन सा है?", "I need an eye checkup", "hospital mein jagah hai?"

4. "farmer" — Questions about farming subsidies, wholesale markets (mandi), crop prices, agricultural schemes
   Examples: "किसान सम्मान निधि के लिए क्या करना होगा?", "mandi bhav kya hai?", "PM Kisan scheme eligibility"

5. "general" — Greetings, general conversation, follow-up questions that don't fit above categories
   Examples: "hello", "thank you", "what can you do?", "aap kaun ho?"

6. "escalate" — The user's question is too specific, complex, or about something you genuinely don't know
   Examples: Questions about very specific local regulations, ongoing legal cases, specific officer contact info

Respond with ONLY the intent label. Nothing else. No explanation.

User's language: {user_language}
User's district: {user_district}"""


SERVICE_NAVIGATOR_PROMPT = """You are JanSeva (जनसेवा), an expert AI assistant for Indian government services.

You help citizens understand:
- What documents and requirements are needed for government services
- Step-by-step process for applications
- Which office/department to visit
- Approximate timelines and fees
- Common mistakes to avoid

IMPORTANT RULES:
1. Always respond in the SAME LANGUAGE the user used (Hindi, English, or mixed).
2. Be specific and actionable — give exact document lists, not vague advice.
3. If you're not sure about a specific local requirement, say so clearly and suggest the user verify with their local office.
4. Include both Hindi and English names for documents when possible.
5. Format your response clearly with bullet points or numbered lists.
6. Never fabricate specific office addresses, phone numbers, or fees — say "check with your local [office name]" instead.

User's language: {user_language}
User's district: {user_district}

If the user asks about generating a form, collect the following information step by step:
- Full name (पूरा नाम)
- Father's/Husband's name (पिता/पति का नाम)
- Date of birth (जन्म तिथि)
- Address (पता)
- Purpose of the document (दस्तावेज का उद्देश्य)

Common government services you should know about:
- Income Certificate (आय प्रमाण पत्र)
- Caste Certificate (जाति प्रमाण पत्र)
- Domicile Certificate (मूल निवासी प्रमाण पत्र)
- Birth Certificate (जन्म प्रमाण पत्र)
- Death Certificate (मृत्यु प्रमाण पत्र)
- Land Records / Khasra-Khatauni (भूमि रिकॉर्ड / खसरा-खतौनी)
- Ration Card (राशन कार्ड)
- Voter ID (मतदाता पहचान पत्र)
- Aadhaar Card updates
- PAN Card
- Passport
- Driving License
"""


GENERAL_CHAT_PROMPT = """You are JanSeva (जनसेवा), a friendly AI assistant for Indian citizens.
You help people navigate government services, report corruption, find healthcare, and assist farmers.

Respond warmly and helpfully in the SAME LANGUAGE the user used.
If asked what you can do, explain your capabilities clearly.
Keep responses concise but helpful.

User's language: {user_language}"""


# --- Node Functions ---

def classify_intent(state: AgentState) -> dict:
    """
    Node: Classify the user's intent.
    Reads the latest message and determines which specialist should handle it.
    """
    llm = get_llm()
    messages = state["messages"]
    latest_message = messages[-1].content if messages else ""
    
    user_language = state.get("user_language", "hi")
    user_district = state.get("user_district", "unknown")

    classification_messages = [
        SystemMessage(content=INTENT_CLASSIFIER_PROMPT.format(
            user_language=user_language,
            user_district=user_district,
        )),
        HumanMessage(content=latest_message),
    ]
    
    response = llm.invoke(classification_messages)
    intent = response.content.strip().lower().replace('"', '').replace("'", "")
    
    # Validate — default to "general" if classification is unexpected
    valid_intents = {"service_query", "anonymous_report", "healthcare", "farmer", "general", "escalate"}
    if intent not in valid_intents:
        logger.warning("unexpected_intent_classification", raw=intent, fallback="general")
        intent = "general"
    
    logger.info("intent_classified", intent=intent, message_preview=latest_message[:50])
    
    return {"intent": intent}


def handle_general_chat(state: AgentState) -> dict:
    """Node: Handle general conversation (greetings, follow-ups, etc.)."""
    llm = get_llm()
    user_language = state.get("user_language", "hi")
    
    system_msg = SystemMessage(content=GENERAL_CHAT_PROMPT.format(
        user_language=user_language,
    ))
    
    # Include recent conversation history for context
    recent_messages = list(state["messages"][-6:])  # Last 6 messages for context
    all_messages = [system_msg] + recent_messages
    
    response = llm.invoke(all_messages)
    
    return {"response": response.content}


def handle_placeholder(state: AgentState) -> dict:
    """
    Placeholder node for agents not yet implemented.
    Used for healthcare, farmer, and anonymous_report until their guides are completed.
    """
    intent = state.get("intent", "unknown")
    user_language = state.get("user_language", "hi")
    
    placeholder_responses = {
        "anonymous_report": (
            "🚨 गुमनाम शिकायत प्रणाली जल्द ही उपलब्ध होगी।\n"
            "Anonymous reporting system coming soon.\n\n"
            "कृपया /report कमांड का उपयोग करें जब यह तैयार हो।"
        ),
        "healthcare": (
            "🏥 स्वास्थ्य सेवा सहायता जल्द ही उपलब्ध होगी।\n"
            "Healthcare assistance coming soon.\n\n"
            "अभी के लिए, अपने नजदीकी सरकारी अस्पताल से संपर्क करें।"
        ),
        "farmer": (
            "🌾 किसान सेवा सहायता जल्द ही उपलब्ध होगी।\n"
            "Farmer services coming soon.\n\n"
            "अभी के लिए, अपने ब्लॉक कृषि अधिकारी से संपर्क करें।"
        ),
    }
    
    return {"response": placeholder_responses.get(intent, "यह सेवा जल्द उपलब्ध होगी।")}


def route_by_intent(state: AgentState) -> str:
    """
    Conditional edge function.
    Routes to the appropriate specialist node based on classified intent.
    """
    intent = state.get("intent", "general")
    
    route_map = {
        "service_query": "service_navigator",
        "anonymous_report": "placeholder",      # TODO: Guide 05
        "healthcare": "placeholder",             # TODO: Guide 09
        "farmer": "placeholder",                 # TODO: Guide 10
        "general": "general_chat",
        "escalate": "escalation",
    }
    
    return route_map.get(intent, "general_chat")


# --- Build the Graph ---

def build_agent_graph() -> StateGraph:
    """
    Construct the full JanSeva agent graph.
    
    Graph structure:
        START → classify_intent → (conditional routing) → [specialist] → END
    """
    graph = StateGraph(AgentState)
    
    # Add nodes
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("service_navigator", handle_service_query)
    graph.add_node("general_chat", handle_general_chat)
    graph.add_node("escalation", handle_escalation)
    graph.add_node("placeholder", handle_placeholder)
    
    # Set entry point
    graph.set_entry_point("classify_intent")
    
    # Add conditional routing from intent classifier
    graph.add_conditional_edges(
        "classify_intent",
        route_by_intent,
        {
            "service_navigator": "service_navigator",
            "general_chat": "general_chat",
            "escalation": "escalation",
            "placeholder": "placeholder",
        },
    )
    
    # All specialist nodes lead to END
    graph.add_edge("service_navigator", END)
    graph.add_edge("general_chat", END)
    graph.add_edge("escalation", END)
    graph.add_edge("placeholder", END)
    
    return graph.compile()


# Module-level compiled graph (singleton)
agent_graph = build_agent_graph()
```

---

### 4. Service Navigator Specialist

**File: `src/janseva/agents/specialists/service_navigator.py`**

```python
"""
Service Navigator Agent — Answers questions about government services.

Handles:
- "What documents do I need for X?"
- "How do I apply for Y?"
- "What is the process for Z?"
- Form generation assistance
"""
from langchain_core.messages import SystemMessage
from janseva.agents.llm import get_llm

# This prompt is imported from the orchestrator for now.
# In Guide 04 (RAG), this will be enhanced with retrieved knowledge base context.

SERVICE_PROMPT = """You are JanSeva (जनसेवा), an expert AI assistant for Indian government services.

You help citizens understand:
- What documents and requirements are needed for government services
- Step-by-step process for applications
- Which office/department to visit
- Approximate timelines and fees

IMPORTANT RULES:
1. Always respond in the SAME LANGUAGE the user used.
2. Be specific — give exact document lists, not vague advice.
3. If unsure about local specifics, say so and suggest verifying locally.
4. Include Hindi and English document names when possible.
5. Use bullet points and numbered lists for clarity.
6. NEVER fabricate specific addresses, phone numbers, or fees.

Common services reference:
- आय प्रमाण पत्र (Income Certificate): SDM/Tehsildar office. Needs: Aadhaar, ration card, self-declaration, salary slip or farm income proof.
- जाति प्रमाण पत्र (Caste Certificate): SDM office. Needs: Aadhaar, father's caste certificate (if available), school records, affidavit.
- मूल निवासी प्रमाण पत्र (Domicile Certificate): Tehsildar. Needs: Aadhaar, voter ID, ration card, electricity/water bill.
- जन्म प्रमाण पत्र (Birth Certificate): Municipal office/Gram Panchayat. Hospital record or affidavit if delayed registration.
- राशन कार्ड (Ration Card): Food & Civil Supplies dept. Needs: Aadhaar of all family members, gas connection details, income proof.
- भूमि रिकॉर्ड (Land Records): Tehsil/Patwari office or state portal (e.g., Bhulekh). Need: Khasra/Khatauni number or name.

User's language: {user_language}
User's district: {user_district}"""


def handle_service_query(state: dict) -> dict:
    """
    Process a government service query.
    
    In Phase 1: Uses LLM with built-in knowledge.
    In Phase 2 (Guide 04): Will add RAG retrieval from knowledge base.
    """
    llm = get_llm()
    user_language = state.get("user_language", "hi")
    user_district = state.get("user_district", "unknown")
    
    system_msg = SystemMessage(content=SERVICE_PROMPT.format(
        user_language=user_language,
        user_district=user_district,
    ))
    
    # Include recent conversation for context
    recent_messages = list(state["messages"][-6:])
    all_messages = [system_msg] + recent_messages
    
    response = llm.invoke(all_messages)
    
    return {"response": response.content}
```

---

### 5. Escalation Specialist (Stub)

**File: `src/janseva/agents/specialists/escalation.py`**

```python
"""
Escalation Agent — Handles queries the AI cannot answer.
Logs the query and routes it to the admin panel for human review.

Full implementation in Guide 06.
"""
import structlog

logger = structlog.get_logger()


def handle_escalation(state: dict) -> dict:
    """
    Handle queries that need human attention.
    
    Phase 1: Log and inform user.
    Phase 2 (Guide 06): Store in DB, notify admin, track resolution.
    """
    latest_message = state["messages"][-1].content if state["messages"] else "unknown"
    user_language = state.get("user_language", "hi")
    
    logger.warning(
        "query_escalated",
        query_preview=latest_message[:100],
        reason="ai_cannot_answer",
    )
    
    response = (
        "🔄 <b>आपका सवाल हमारी टीम को भेज दिया गया है।</b>\n\n"
        "यह सवाल हमारे AI के दायरे से बाहर है। हमारी प्रशासनिक टीम "
        "इसकी जाँच करेगी और जल्द से जल्द आपको जवाब देगी।\n\n"
        "📝 आपका सवाल दर्ज कर लिया गया है। आपको अपडेट मिलेगा।\n\n"
        "<i>Your query has been forwarded to our team. "
        "They will review it and get back to you soon.</i>"
    )
    
    return {
        "response": response,
        "needs_escalation": True,
        "escalation_reason": "AI could not provide a confident answer",
    }
```

---

### 6. Agent Service (Bridge between Telegram and LangGraph)

**File: `src/janseva/agents/service.py`**

```python
"""
Agent Service — The bridge between the Telegram bot and the LangGraph agent.

This module provides a clean interface:
    process_message(telegram_id, text, language) → response_text

It handles:
- Loading/creating conversation state
- Running the agent graph
- Storing messages in the database
- Returning the final response
"""
import uuid
import structlog
from langchain_core.messages import HumanMessage

from janseva.agents.orchestrator import agent_graph
from janseva.db.engine import async_session_factory
from janseva.db.models.user import User
from janseva.db.models.conversation import Conversation
from janseva.db.models.message import Message

from sqlalchemy import select

logger = structlog.get_logger()


async def process_message(
    telegram_id: int,
    user_text: str,
    language: str = "hi",
    district: str = "unknown",
) -> str:
    """
    Process a user's text message through the AI agent pipeline.
    
    Args:
        telegram_id: User's Telegram ID
        user_text: The text message from the user
        language: Detected/preferred language code
        district: User's district for localized results
    
    Returns:
        The AI agent's response text
    """
    async with async_session_factory() as session:
        # 1. Find the user
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        
        if user is None:
            logger.error("user_not_found", telegram_id=telegram_id)
            return "❌ कृपया पहले /start कमांड भेजें। Please send /start first."
        
        # 2. Find or create an active conversation
        result = await session.execute(
            select(Conversation)
            .where(Conversation.user_id == user.id)
            .where(Conversation.status == "active")
            .order_by(Conversation.created_at.desc())
        )
        conversation = result.scalar_one_or_none()
        
        if conversation is None:
            conversation = Conversation(
                user_id=user.id,
                agent_type="orchestrator",
                status="active",
            )
            session.add(conversation)
            await session.flush()  # Get the ID
        
        # 3. Store the user's message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=user_text,
            language=language,
        )
        session.add(user_message)
        
        # 4. Load recent conversation history for context
        result = await session.execute(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.desc())
            .limit(10)  # Last 10 messages for context
        )
        recent_messages = list(reversed(result.scalars().all()))
        
        # Convert DB messages to LangChain format
        langchain_messages = []
        for msg in recent_messages:
            if msg.role == "user":
                langchain_messages.append(HumanMessage(content=msg.content))
            else:
                from langchain_core.messages import AIMessage
                langchain_messages.append(AIMessage(content=msg.content))
        
        # 5. Run the agent graph
        try:
            initial_state = {
                "messages": langchain_messages,
                "user_language": user.language or language,
                "user_district": user.district or district,
                "user_telegram_id": telegram_id,
                "intent": "",
                "response": "",
                "needs_escalation": False,
                "escalation_reason": "",
            }
            
            result_state = agent_graph.invoke(initial_state)
            response_text = result_state.get("response", "")
            
            if not response_text:
                response_text = (
                    "🤔 मुझे इस सवाल का जवाब नहीं मिल पाया। "
                    "कृपया दोबारा कोशिश करें या /help टाइप करें।"
                )
            
        except Exception as e:
            logger.error("agent_error", error=str(e), telegram_id=telegram_id)
            response_text = (
                "⚠️ कुछ गड़बड़ हो गई। कृपया थोड़ी देर बाद दोबारा कोशिश करें।\n"
                "Something went wrong. Please try again in a moment."
            )
        
        # 6. Store the assistant's response
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=response_text,
            language=user.language or language,
        )
        session.add(assistant_message)
        await session.commit()
        
        logger.info(
            "message_processed",
            telegram_id=telegram_id,
            intent=result_state.get("intent", "unknown") if 'result_state' in dir() else "error",
            response_length=len(response_text),
        )
        
        return response_text
```

---

### 7. Update Telegram Text Handler to Use the Agent

**File: `src/janseva/bot/routers/text.py`** — REPLACE the entire file with:

```python
"""
Handles all text messages that are not commands.
Forwards messages to the LangGraph agent pipeline and returns the response.
"""
import structlog
from aiogram import Router, F
from aiogram.types import Message

from janseva.agents.service import process_message

logger = structlog.get_logger()

text_router = Router(name="text")


@text_router.message(F.text)
async def handle_text_message(message: Message) -> None:
    """
    Handle incoming text messages.
    Forwards to the AI agent orchestrator and returns the response.
    """
    if not message.text or not message.from_user:
        return

    user_text = message.text.strip()
    telegram_id = message.from_user.id

    # Skip empty messages
    if not user_text:
        return

    logger.info(
        "text_message_received",
        telegram_id=telegram_id,
        text_length=len(user_text),
    )

    # Show "typing" indicator while AI processes
    await message.chat.do(action="typing")

    # Process through AI agent pipeline
    response = await process_message(
        telegram_id=telegram_id,
        user_text=user_text,
    )

    # Send response (split if too long for Telegram's 4096 char limit)
    if len(response) <= 4096:
        await message.answer(response)
    else:
        # Split into chunks
        for i in range(0, len(response), 4096):
            chunk = response[i:i + 4096]
            await message.answer(chunk)
```

---

## How It All Connects

```
User sends "आय प्रमाण पत्र के लिए क्या चाहिए?" on Telegram
    │
    ▼
aiogram text_router.handle_text_message()
    │
    ▼
agents.service.process_message()
    ├── Finds/creates user + conversation in DB
    ├── Loads recent message history
    ├── Runs agent_graph.invoke()
    │       │
    │       ▼
    │   classify_intent node
    │       ├── LLM sees: "government service question"
    │       └── Returns: intent = "service_query"
    │       │
    │       ▼ (conditional edge)
    │   service_navigator node
    │       ├── LLM with SERVICE_PROMPT + conversation history
    │       └── Returns: detailed response about income certificate requirements
    │       │
    │       ▼
    │   END
    │
    ├── Stores user message + AI response in DB
    └── Returns response text
    │
    ▼
Bot sends response to user on Telegram
```

---

## Verification Checklist

After implementing this guide:

- [ ] Bot responds intelligently to "आय प्रमाण पत्र के लिए क्या चाहिए?"
- [ ] Bot responds in the same language the user uses
- [ ] Bot handles greetings ("hello", "namaste") with general chat
- [ ] Bot shows placeholder for anonymous reports, healthcare, farmer queries
- [ ] Bot escalates truly unknown queries with a polite message
- [ ] Conversation history is stored in PostgreSQL (`messages` table)
- [ ] "Typing" indicator shows while AI is processing
- [ ] Long responses are split at 4096 characters
- [ ] Errors don't crash the bot — user gets a friendly error message

---

## Testing the Intent Classifier

Send these test messages and verify correct routing:

| Message | Expected Intent | Expected Behavior |
|---------|----------------|-------------------|
| "आय प्रमाण पत्र कैसे बनाएं?" | `service_query` | Detailed requirements list |
| "Income certificate requirements" | `service_query` | Detailed requirements list |
| "मुझे एक शिकायत करनी है" | `anonymous_report` | Placeholder: "coming soon" |
| "नजदीकी अस्पताल कहाँ है?" | `healthcare` | Placeholder: "coming soon" |
| "PM Kisan scheme eligibility" | `farmer` | Placeholder: "coming soon" |
| "hello" | `general` | Friendly greeting + capabilities |
| "What is the exact phone number of the Lucknow DM office?" | `escalate` | Escalation message |

---

## Git Checkpoint

```bash
git add -A
git commit -m "feat(agents): implement LangGraph orchestrator with intent routing

- LangGraph state schema (AgentState) with conversation context
- LLM provider factory (Gemini + Ollama support)
- Orchestrator agent: intent classification → conditional routing
- Service Navigator specialist: government service Q&A
- Escalation specialist: logs unhandled queries
- Agent service bridge: Telegram → Agent → DB → Response
- Conversation memory via PostgreSQL message history
- Updated text handler to use agent pipeline"
```
