"""
Handles all text messages that are not commands.
Forwards messages to the LangGraph agent pipeline and returns the response.
"""
import structlog
from aiogram import Router, F
from aiogram.types import Message

from janseva.agents.service import process_message
from janseva.bot.helpers.feedback import send_thinking, update_with_response, send_error
from janseva.db.engine import async_session_factory
from janseva.db.models.user import User
from sqlalchemy import select

logger = structlog.get_logger()

text_router = Router(name="text")


@text_router.message(F.text)
async def handle_text_message(message: Message) -> None:
    """
    Handle incoming text messages.
    Forwards to the AI agent orchestrator and returns the response.
    """
    if not message.text or not message.from_user:
        return

    user_text = message.text.strip()
    telegram_id = message.from_user.id

    # Skip empty messages
    if not user_text:
        return

    logger.info(
        "text_message_received",
        telegram_id=telegram_id,
        text_length=len(user_text),
    )

    # 1. Check onboarding status
    async with async_session_factory() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        
        if not user or not user.onboarding_complete:
            # Send them to the onboarding flow
            from janseva.bot.routers.start import handle_start
            await handle_start(message)
            return

    # Show "thinking" indicator with actual message
    thinking_msg = await send_thinking(message)

    from janseva.notifications.profiler import update_user_interests
    import asyncio
    
    # Process through AI agent pipeline
    try:
        response = await process_message(
            telegram_id=telegram_id,
            user_text=user_text,
        )
        
        # Fire and forget updating interests
        asyncio.create_task(update_user_interests(telegram_id, user_text))

        # Edit the thinking message with the response
        await update_with_response(message, thinking_msg, response)
        
    except Exception as e:
        logger.error("error_processing_text", error=str(e), telegram_id=telegram_id)
        await send_error(message, language=user.language if user else "hi")
