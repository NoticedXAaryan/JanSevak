"""
Healthcare Agent — Specialist agent for finding hospitals and booking appointments.
"""
import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import random

from janseva.db.engine import async_session_factory
from janseva.db.models.healthcare_facility import HealthcareFacility
from janseva.agents.llm import get_llm

logger = structlog.get_logger()

async def find_facilities(district: str, limit: int = 3) -> list[HealthcareFacility]:
    """Find accepting healthcare facilities in a given district."""
    async with async_session_factory() as session:
        # Simple search by district. In a real app, this would use pgvector or postgis for nearest
        stmt = select(HealthcareFacility).where(
            HealthcareFacility.district.ilike(f"%{district}%"),
            HealthcareFacility.is_accepting_patients == True
        ).limit(limit)
        
        result = await session.execute(stmt)
        return list(result.scalars().all())

async def handle_healthcare_query(state: dict) -> dict:
    """
    Process a healthcare related query.
    Extracts the intent (search/book), finds facilities, and generates response.
    """
    llm = get_llm()
    user_language = state.get("user_language", "hi")
    latest_message = state["messages"][-1].content if state["messages"] else ""
    user_district = state.get("user_district", "Bhopal") # Default to Bhopal for demo if not set
    
    # 1. Fetch facilities from database
    facilities = await find_facilities(user_district)
    
    # 2. Build context from facilities
    facility_context = ""
    if facilities:
        for idx, f in enumerate(facilities):
            specialties = ", ".join(f.specialties) if f.specialties else "General"
            facility_context += f"{idx+1}. {f.name} ({f.facility_type})\n   Beds Available: {f.available_beds}/{f.total_beds}\n   Specialties: {specialties}\n   Address: {f.address}\n\n"
    else:
        facility_context = "No facilities found in your area."
        
    # Generate a random queue number for demonstration if the user wants to book
    queue_number = random.randint(10, 99)
    
    # 3. LLM call to generate a friendly response
    prompt = f"""
You are JanSeva's Healthcare Assistant. 
The user said: "{latest_message}"
Their district is: {user_district}

Here are the nearest available facilities:
{facility_context}

RULES:
1. Respond in the user's language: {user_language}
2. If they are asking to find a hospital, list the available facilities clearly with their bed availability.
3. If they are asking to book an appointment, generate a confirmation for the first available facility and give them Queue Number: {queue_number}. Tell them the estimated wait time is ~45 minutes.
4. Be empathetic and clear.
"""
    
    # We use a simple invoke for this specialist
    response = await llm.ainvoke(prompt)
    
    logger.info(
        "healthcare_agent_invoked",
        district=user_district,
        facilities_found=len(facilities)
    )
    
    return {"response": response.content}
