"""
Farmer Services Agent — Specialist agent for agricultural queries.
Handles subsidy information and Mandi (wholesale market) prices.
"""
import os
import yaml
import structlog
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from janseva.db.engine import async_session_factory
from janseva.db.models.mandi_price import MandiPrice
from janseva.agents.llm import get_llm

logger = structlog.get_logger()

# Load static subsidies from knowledge base
def load_subsidies() -> list[dict]:
    subsidies = []
    base_dir = Path(os.path.dirname(__file__)).parent.parent / "knowledge" / "data" / "subsidies"
    if base_dir.exists():
        for yaml_file in base_dir.glob("*.yaml"):
            try:
                with open(yaml_file, "r", encoding="utf-8") as f:
                    subsidies.append(yaml.safe_load(f))
            except Exception as e:
                logger.error("failed_to_load_subsidy", file=str(yaml_file), error=str(e))
    return subsidies


async def get_mandi_prices(district: str, limit: int = 5) -> list[MandiPrice]:
    """Fetch recent mandi prices for a given district."""
    async with async_session_factory() as session:
        stmt = select(MandiPrice).where(
            MandiPrice.district.ilike(f"%{district}%")
        ).order_by(MandiPrice.date.desc()).limit(limit)
        
        result = await session.execute(stmt)
        return list(result.scalars().all())


async def handle_farmer_query(state: dict) -> dict:
    """
    Process an agricultural query.
    Extracts the intent (subsidy vs mandi price), fetches data, and generates response.
    """
    llm = get_llm()
    user_language = state.get("user_language", "hi")
    latest_message = state["messages"][-1].content if state["messages"] else ""
    user_district = state.get("user_district", "Bhopal") # Default to Bhopal for demo if not set
    
    # 1. Load Subsidy Data
    subsidies = load_subsidies()
    subsidy_context = ""
    for sub in subsidies:
        subsidy_context += f"- **{sub.get('name_hi', sub.get('name_en'))}**: {sub.get('benefit', '')}\n"
        subsidy_context += f"  Eligibility: {', '.join(sub.get('eligibility', []))}\n"
        subsidy_context += f"  Documents: {', '.join(sub.get('required_documents', []))}\n"
        subsidy_context += f"  Process: {', '.join(sub.get('application_process', []))}\n\n"

    # 2. Fetch Mandi Prices
    prices = await get_mandi_prices(user_district)
    price_context = ""
    if prices:
        for p in prices:
            crop = p.crop_name_hi if p.crop_name_hi else p.crop_name
            price_context += f"- {crop} in {p.market_name} ({p.date}): ₹{p.modal_price}/quintal (Min: ₹{p.min_price}, Max: ₹{p.max_price})\n"
    else:
        price_context = "No mandi prices available for your district today."
        
    # 3. LLM call to generate response
    prompt = f"""
You are JanSeva's Farmer Services Assistant (Kisan Sahayak).
The user said: "{latest_message}"
Their district is: {user_district}

Here is the current information you can use to answer:

MANDI PRICES (Wholesale Market):
{price_context}

GOVERNMENT SUBSIDIES & SCHEMES:
{subsidy_context}

RULES:
1. Respond in the user's language: {user_language}
2. If they are asking about crop prices, check the MANDI PRICES section and provide the rates.
3. If they are asking about PM-Kisan, subsidies, or schemes, explain the eligibility and application process clearly from the GOVERNMENT SUBSIDIES section.
4. Keep the tone helpful, respectful, and easy to understand for a farmer.
5. If the requested information is not in the context, politely state that you don't have that specific data right now but provide the helpline (e.g. 155261 for PM-Kisan) if relevant.
"""
    
    response = await llm.ainvoke(prompt)
    
    logger.info(
        "farmer_agent_invoked",
        district=user_district,
        prices_found=len(prices),
        subsidies_loaded=len(subsidies)
    )
    
    return {"response": response.content}
