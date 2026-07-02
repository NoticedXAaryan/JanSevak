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
