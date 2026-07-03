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
from janseva.agents.specialists.anonymous_reporter import handle_anonymous_report

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
        "anonymous_report": "anonymous_report_node",
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
    graph.add_node("anonymous_report_node", handle_anonymous_report)
    graph.add_node("placeholder", handle_placeholder)
    
    # Set entry point
    graph.set_entry_point("classify_intent")
    
    # Add conditional routing from intent classifier
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
    
    # All specialist nodes lead to END
    graph.add_edge("service_navigator", END)
    graph.add_edge("anonymous_report_node", END)
    graph.add_edge("general_chat", END)
    graph.add_edge("escalation", END)
    graph.add_edge("placeholder", END)
    
    return graph.compile()


# Module-level compiled graph (singleton)
agent_graph = build_agent_graph()
