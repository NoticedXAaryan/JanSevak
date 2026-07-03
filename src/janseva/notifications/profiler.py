"""Interest Profiler for User Queries."""
import logging
from typing import List
from pydantic import BaseModel, Field

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from janseva.config import settings
from janseva.db.engine import async_session_factory
from janseva.db.models.user import User

logger = logging.getLogger(__name__)

class ExtractedInterests(BaseModel):
    topics: List[str] = Field(description="A list of 1-3 broad topics related to the user's query. Examples: 'agriculture', 'healthcare', 'education', 'subsidies', 'documents'. Use lowercase.")

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an assistant that analyzes user queries to government service bots and extracts broad interest categories. Return a list of 1 to 3 relevant topics in lowercase. Do not extract highly specific terms; use broad categories like 'agriculture', 'healthcare', 'education', 'employment', 'subsidies', 'pensions', 'documents'."),
    ("human", "{query}")
])

async def extract_interests(query: str) -> List[str]:
    """Use Gemini to extract interests from a query string."""
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.gemini_api_key,
            temperature=0
        )
        structured_llm = llm.with_structured_output(ExtractedInterests)
        chain = prompt_template | structured_llm
        
        result = await chain.ainvoke({"query": query})
        if result and isinstance(result, ExtractedInterests):
            return result.topics
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
                update(User)
                .where(User.telegram_id == telegram_id)
                .values(interests=updated_list)
            )
            await session.commit()
            logger.info(f"Updated interests for user {telegram_id}: {updated_list}")
