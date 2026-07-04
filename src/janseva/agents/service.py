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
        
        from janseva.common.cache import query_cache
        
        # Check cache for identical queries
        cached_response = await query_cache.get(user_text)
        if cached_response:
            logger.info("cache_hit", telegram_id=telegram_id)
            
            # Still store the messages in DB for history
            assistant_message = Message(
                conversation_id=conversation.id,
                role="assistant",
                content=cached_response,
                language=user.language or language,
            )
            session.add(assistant_message)
            await session.commit()
            return cached_response, []
        
        # 5. Run the agent graph
        interactive_options = []
        try:
            initial_state = {
                "messages": langchain_messages,
                "user_language": user.language or language,
                "user_district": user.district or district,
                "user_telegram_id": telegram_id,
                "intent": "",
                "response": "",
                "interactive_options": [],
                "needs_escalation": False,
                "escalation_reason": "",
            }
            
            result_state = agent_graph.invoke(initial_state)
            response_text = result_state.get("response", "")
            interactive_options = result_state.get("interactive_options", [])
            
            if not response_text:
                response_text = (
                    "🤔 मुझे इस सवाल का जवाब नहीं मिल पाया। "
                    "कृपया दोबारा कोशिश करें या /help टाइप करें।"
                )
            
            # Save to cache on success
            await query_cache.set(user_text, response_text)
            
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
            intent=result_state.get("intent", "unknown") if 'result_state' in locals() else "error",
            response_length=len(response_text),
            options_count=len(interactive_options)
        )
        
        return response_text, interactive_options
