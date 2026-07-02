"""
Service Navigator Agent — Enhanced with RAG.
Retrieves relevant knowledge base entries and uses them to provide
accurate, sourced answers about government services.
"""
from langchain_core.messages import SystemMessage
from janseva.agents.llm import get_llm
from janseva.agents.tools.knowledge_search import search_services


SERVICE_RAG_PROMPT = """You are JanSeva (जनसेवा), an expert AI assistant for Indian government services.

You have access to a curated knowledge base about government services.
Below is relevant information retrieved from the knowledge base for this query:

--- KNOWLEDGE BASE CONTEXT ---
{knowledge_context}
--- END CONTEXT ---

RULES:
1. ALWAYS respond in the SAME LANGUAGE the user used (Hindi, English, or mixed).
2. Use the knowledge base context above as your PRIMARY source of information.
3. If the context contains specific requirements, list them exactly as documented.
4. If the context doesn't cover the question, say so clearly and suggest checking locally.
5. NEVER fabricate specific addresses, phone numbers, or fees not in the context.
6. Format with bullet points and numbered lists for clarity.
7. Include both Hindi and English names when available in the context.

User's language: {user_language}
User's district: {user_district}"""


def handle_service_query(state: dict) -> dict:
    """
    Process a government service query using RAG.
    
    1. Search the knowledge base for relevant information
    2. Augment the LLM prompt with retrieved context
    3. Generate a response grounded in the knowledge base
    """
    llm = get_llm()
    user_language = state.get("user_language", "hi")
    user_district = state.get("user_district", "unknown")
    
    # Get the latest user message
    latest_message = state["messages"][-1].content if state["messages"] else ""
    
    # RAG: Search knowledge base
    knowledge_context = search_services(latest_message)
    
    # Build the prompt with retrieved context
    system_msg = SystemMessage(content=SERVICE_RAG_PROMPT.format(
        knowledge_context=knowledge_context,
        user_language=user_language,
        user_district=user_district,
    ))
    
    # Include recent conversation for context
    recent_messages = list(state["messages"][-6:])
    all_messages = [system_msg] + recent_messages
    
    response = llm.invoke(all_messages)
    
    return {"response": response.content}
