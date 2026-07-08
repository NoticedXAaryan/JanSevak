"""Interest Profiler for User Queries."""

import logging

from langchain_core.messages import HumanMessage, SystemMessage
from sqlalchemy import select, update

from janseva.agents.llm import get_llm
from janseva.db.engine import async_session_factory
from janseva.db.models.user import User

logger = logging.getLogger(__name__)

INTEREST_EXTRACTION_PROMPT = """You are an assistant that analyzes user queries to government service bots and extracts broad interest categories. Return ONLY a comma-separated list of 1 to 3 relevant topics in lowercase. Do not include any other text.

Valid topics: agriculture, healthcare, education, employment, subsidies, pensions, documents, housing, women_welfare, farmer, banking, legal, transport, business, disability, senior_citizen

Example input: "How to apply for PM-KISAN?"
Example output: agriculture, subsidies, farmer

Query: {query}"""


async def extract_interests(query: str) -> list[str]:
    """Use the configured LLM to extract interests from a query string."""
    try:
        llm = get_llm()

        messages = [
            SystemMessage(
                content="You extract broad topic categories from user queries. Return ONLY a comma-separated list of 1-3 topics. No other text."
            ),
            HumanMessage(content=INTEREST_EXTRACTION_PROMPT.format(query=query)),
        ]

        result = await llm.ainvoke(messages)
        if result and result.content:
            # Parse comma-separated topics
            topics = [t.strip().lower() for t in result.content.split(",") if t.strip()]
            # Filter to valid topics only
            valid = {
                "agriculture",
                "healthcare",
                "education",
                "employment",
                "subsidies",
                "pensions",
                "documents",
                "housing",
                "women_welfare",
                "farmer",
                "banking",
                "legal",
                "transport",
                "business",
                "disability",
                "senior_citizen",
            }
            return [t for t in topics if t in valid][:3]
    except Exception as e:
        logger.error(f"Error extracting interests: {e}")
    return []


async def update_user_interests(telegram_id: int, query: str):
    """
    Fire-and-forget function to update a user's interests based on their query.
    """
    topics = await extract_interests(query)
    if not topics:
        return

    async with async_session_factory() as session:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            current_interests = set(user.interests or [])
            new_interests = current_interests.union(set(topics))

            # Keep max 10 interests to avoid bloating
            updated_list = list(new_interests)[:10]

            await session.execute(
                update(User).where(User.telegram_id == telegram_id).values(interests=updated_list)
            )
            await session.commit()
            logger.info(f"Updated interests for user {telegram_id}: {updated_list}")
