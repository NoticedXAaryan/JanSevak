#!/usr/bin/env python3
import asyncio
from unittest.mock import patch

from dotenv import load_dotenv

load_dotenv()

from langchain_core.documents import Document
from langchain_core.messages import HumanMessage

from janseva.agents.orchestrator import agent_graph


async def run_scenario(name, prompt):
    print(f"\n{'=' * 50}")
    print(f"SCENARIO: {name}")
    print(f"USER PROMPT: {prompt}")
    print(f"{'=' * 50}")

    initial_state = {
        "messages": [HumanMessage(content=prompt)],
        "user_language": "en",
        "user_district": "Bhopal",
        "user_telegram_id": 123,
        "intent": "",
        "response": "",
        "needs_escalation": False,
        "escalation_reason": "",
    }

    from janseva.db.models.healthcare_facility import HealthcareFacility
    from janseva.db.models.mandi_price import MandiPrice

    mock_mandi = [
        MandiPrice(
            crop_name="Wheat",
            crop_name_hi="गेहूँ",
            market_name="Bhopal Mandi",
            modal_price=2500,
            min_price=2400,
            max_price=2600,
            date="2026-07-04",
        )
    ]

    mock_hospital = [
        HealthcareFacility(
            name="Bhopal City Hospital",
            facility_type="General",
            available_beds=45,
            total_beds=200,
            specialties=["General", "Eye Care"],
            address="123 Health Ave",
        )
    ]

    # Run the graph inside a patch to mock RAG embeddings and DB calls
    with (
        patch("janseva.knowledge.vector_store.search_knowledge") as mock_search,
        patch("janseva.agents.specialists.farmer_agent.get_mandi_prices") as mock_mandi_call,
        patch("janseva.agents.specialists.healthcare_agent.find_facilities") as mock_health_call,
    ):
        mock_search.return_value = [
            (
                Document(
                    page_content="The Mudra loan scheme requires Aadhaar, PAN, and business plan.",
                    metadata={"source": "mudra.pdf"},
                ),
                0.9,
            ),
            (
                Document(
                    page_content="Housing loan applications require income proof and property documents.",
                    metadata={"source": "housing.pdf"},
                ),
                0.8,
            ),
        ]
        mock_mandi_call.return_value = mock_mandi
        mock_health_call.return_value = mock_hospital

        result = await agent_graph.ainvoke(initial_state)

    intent = result.get("intent", "Unknown")
    response = result.get("response", "No response generated.")

    print(f"\nCLASSIFIED INTENT: {intent}")
    print(f"\nRESPONSE:\n{response}")
    print(f"{'=' * 50}\n")


async def main():
    scenarios = [
        ("Loan Scheme Requirements", "What are the requirements for the Mudra loan scheme?"),
        (
            "Housing Loan Applicability",
            "I want to apply for a housing loan plan. Which ones am I eligible for?",
        ),
        ("Farmer Mandi Inquiry", "mandi bhav kya hai? what is the local market price for wheat?"),
        (
            "Hospital Booking",
            "I am feeling sick and need to book an eye appointment at the nearest hospital. Can you help me?",
        ),
    ]

    for name, prompt in scenarios:
        await run_scenario(name, prompt)


if __name__ == "__main__":
    asyncio.run(main())
