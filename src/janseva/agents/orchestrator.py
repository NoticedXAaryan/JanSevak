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
from langgraph.graph import END, StateGraph

from janseva.agents.llm import get_llm
from janseva.agents.specialists.anonymous_reporter import handle_anonymous_report
from janseva.agents.specialists.escalation import handle_escalation
from janseva.agents.specialists.farmer_agent import handle_farmer_query
from janseva.agents.specialists.healthcare_agent import handle_healthcare_query
from janseva.agents.specialists.service_navigator import handle_service_query
from janseva.agents.state import AgentState

logger = structlog.get_logger()

# --- System Prompts ---

INTENT_CLASSIFIER_PROMPT = """You are JanSeva (जनसेवा), an AI assistant that helps Indian citizens interact with government services.

Your job is to classify the user's LATEST message into one of these intents.
IMPORTANT: You will also see recent conversation history. Use it to understand context.
If the latest message is a follow-up to a previous topic (e.g., "But I need the government one", "tell me more", "what about the fees?"), classify it based on the ORIGINAL topic, not as "clarify" or "general".

1. "service_query" — Questions about government services, documents, certificates, requirements, applications, forms, government schemes, loans, subsidies
   Examples: "आय प्रमाण पत्र कैसे बनाएं?", "What documents for caste certificate?", "But I need the government scheme", "tell me more about that"

2. "anonymous_report" — User wants to report corruption, misconduct, or wrongdoing anonymously
   Examples: "मुझे एक शिकायत दर्ज करनी है", "I want to report a corrupt officer"

3. "healthcare" — Questions about hospitals, doctors, appointments, medical facilities
   Examples: "नजदीकी अस्पताल कौन सा है?", "I need an eye checkup"

4. "farmer" — Questions about farming subsidies, wholesale markets (mandi), crop prices, agricultural schemes
   Examples: "किसान सम्मान निधि के लिए क्या करना होगा?", "mandi bhav kya hai?"

5. "general" — ONLY greetings, thanks, or asking what the bot can do. NOT follow-ups to previous topics.
   Examples: "hello", "thank you", "what can you do?"

6. "escalate" — The user's question is too specific, complex, or about something you genuinely don't know
   Examples: Questions about very specific local regulations, ongoing legal cases

7. "clarify" — The user's message is genuinely too vague AND there is no prior context to infer meaning from
   Examples: "help" (with no prior messages), single word with no context

Respond with ONLY the intent label. Nothing else. No explanation.

User's language: {user_language}
User's district: {user_district}
Location context: {location_context}"""


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


def load_location_context(state: AgentState) -> dict:
    """
    Node: Load specific context based on the user's location.
    Queries the knowledge base or departments table to inject state/district specific rules
    before the agent processes the request.
    """
    user_district = state.get("user_district", "unknown")

    # In a full implementation, this would query the DB for Department policies in this district.
    # For now, we stub it out with generic regional knowledge if we recognize the region.
    context = ""
    if user_district.lower() in ["lucknow", "kanpur", "varanasi", "agra"]:
        context = "User is in Uttar Pradesh. Use UP specific e-district portal (edistrict.up.gov.in) for revenue services."
    elif user_district.lower() in ["bhopal", "indore", "gwalior"]:
        context = "User is in Madhya Pradesh. Use MP e-district portal (mpedistrict.gov.in)."

    return {"location_context": context}


def classify_intent(state: AgentState) -> dict:
    """
    Node: Classify the user's intent.
    Reads the latest message AND recent history for context-aware classification.
    """
    llm = get_llm()
    messages = state["messages"]
    latest_message = messages[-1].content if messages else ""

    user_language = state.get("user_language", "hi")
    user_district = state.get("user_district", "unknown")
    location_context = state.get("location_context", "")

    # Build context: include last 3 messages so follow-ups have context
    # e.g., "education loan" -> "But I needed Govt one" stays as service_query
    recent_messages = messages[-3:] if len(messages) >= 3 else messages
    context_text = "\n".join(
        f"{'User' if hasattr(m, 'type') and m.type == 'human' else 'Assistant'}: {m.content}"
        for m in recent_messages
    )

    classification_messages = [
        SystemMessage(
            content=INTENT_CLASSIFIER_PROMPT.format(
                user_language=user_language,
                user_district=user_district,
                location_context=location_context,
            )
        ),
        HumanMessage(
            content=f"Recent conversation:\n{context_text}\n\nClassify the LATEST message."
        ),
    ]

    response = llm.invoke(classification_messages)
    intent = response.content.strip().lower().replace('"', "").replace("'", "")

    # Validate — default to "general" if classification is unexpected
    valid_intents = {
        "service_query",
        "anonymous_report",
        "healthcare",
        "farmer",
        "general",
        "escalate",
        "clarify",
    }
    if intent not in valid_intents:
        logger.warning("unexpected_intent_classification", raw=intent, fallback="general")
        intent = "general"

    logger.info("intent_classified", intent=intent, message_preview=latest_message[:50])

    return {"intent": intent}


def handle_general_chat(state: AgentState) -> dict:
    """Node: Handle general conversation (greetings, follow-ups, etc.)."""
    llm = get_llm()
    user_language = state.get("user_language", "hi")

    system_msg = SystemMessage(
        content=GENERAL_CHAT_PROMPT.format(
            user_language=user_language,
        )
    )

    # Include recent conversation history for context
    recent_messages = list(state["messages"][-6:])  # Last 6 messages for context
    all_messages = [system_msg] + recent_messages

    response = llm.invoke(all_messages)

    return {"response": response.content}


def handle_clarification(state: AgentState) -> dict:
    """Node: Ask the user a clarifying question, using conversation history."""
    llm = get_llm()
    user_language = state.get("user_language", "hi")

    prompt = (
        f"You are JanSeva. The user's message was too vague or short. "
        f"Respond in {user_language}. Look at the conversation history for context. "
        f"Ask a short, polite follow-up question to clarify what government service, "
        f"hospital, or report they need help with."
    )

    system_msg = SystemMessage(content=prompt)
    # Include recent history so clarification is context-aware
    recent_messages = list(state["messages"][-4:])
    messages = [system_msg] + recent_messages

    response = llm.invoke(messages)
    return {"response": response.content}





def route_by_intent(state: AgentState) -> str:
    """
    Conditional edge function.
    Routes to the appropriate specialist node based on classified intent.
    """
    intent = state.get("intent", "general")

    route_map = {
        "service_query": "service_navigator",
        "anonymous_report": "anonymous_report_node",
        "healthcare": "healthcare_agent_node",
        "farmer": "farmer_agent_node",
        "general": "general_chat",
        "escalate": "escalation",
        "clarify": "clarification",
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
    graph.add_node("load_location_context", load_location_context)
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("service_navigator", handle_service_query)
    graph.add_node("general_chat", handle_general_chat)
    graph.add_node("escalation", handle_escalation)
    graph.add_node("anonymous_report_node", handle_anonymous_report)
    graph.add_node("healthcare_agent_node", handle_healthcare_query)
    graph.add_node("farmer_agent_node", handle_farmer_query)
    graph.add_node("clarification", handle_clarification)


    # Set entry point
    graph.set_entry_point("load_location_context")
    graph.add_edge("load_location_context", "classify_intent")

    # Add conditional routing from intent classifier
    graph.add_conditional_edges(
        "classify_intent",
        route_by_intent,
        {
            "service_navigator": "service_navigator",
            "anonymous_report_node": "anonymous_report_node",
            "healthcare_agent_node": "healthcare_agent_node",
            "farmer_agent_node": "farmer_agent_node",
            "general_chat": "general_chat",
            "escalation": "escalation",
            "clarification": "clarification",
        },
    )

    # All specialist nodes lead to END
    graph.add_edge("service_navigator", END)
    graph.add_edge("anonymous_report_node", END)
    graph.add_edge("healthcare_agent_node", END)
    graph.add_edge("farmer_agent_node", END)
    graph.add_edge("general_chat", END)
    graph.add_edge("escalation", END)
    graph.add_edge("clarification", END)


    return graph.compile()


# Module-level compiled graph (singleton)
agent_graph = build_agent_graph()
