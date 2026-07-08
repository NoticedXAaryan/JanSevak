"""
Handles all text messages that are not commands.
Forwards messages to the LangGraph agent pipeline and returns the response.
"""

import structlog
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select

from janseva.agents.service import process_message
from janseva.bot.helpers.feedback import send_error, send_thinking, update_with_response
from janseva.db.engine import async_session_factory
from janseva.db.models.user import User

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

    import asyncio

    from janseva.notifications.profiler import update_user_interests

    # Process through AI agent pipeline
    try:
        response_text, interactive_options = await process_message(
            telegram_id=telegram_id,
            user_text=user_text,
        )

        # Fire and forget updating interests
        asyncio.create_task(update_user_interests(telegram_id, user_text))

        # Build inline keyboard if we have interactive options
        reply_markup = None
        if interactive_options:
            from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

            buttons = [
                [InlineKeyboardButton(text=opt["text"], callback_data=opt["callback_data"])]
                for opt in interactive_options
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        # Edit the thinking message with the response
        await update_with_response(message, thinking_msg, response_text, reply_markup=reply_markup)

    except Exception as e:
        logger.error("error_processing_text", error=str(e), telegram_id=telegram_id)
        await send_error(message, language=user.language if user else "hi")


@text_router.callback_query(F.data.startswith("query_"))
async def handle_scheme_query_callback(callback: CallbackQuery):
    """
    Handle clicks on interactive scheme buttons.
    Treats the click exactly as if the user typed "Tell me about <Scheme Name>".
    """
    if not callback.message or not callback.from_user:
        return

    scheme_name = callback.data.split("_", 1)[1]
    telegram_id = callback.from_user.id

    # Let the user know we received the click
    await callback.answer(f"Fetching details for {scheme_name}...")

    # Construct a synthetic user message
    user_text = f"Tell me about {scheme_name}"

    # Send a new thinking message
    thinking_msg = await send_thinking(callback.message)

    # Get user language for error handling
    language = "hi"
    async with async_session_factory() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if user and user.language:
            language = user.language

    import asyncio

    from janseva.notifications.profiler import update_user_interests

    try:
        response_text, interactive_options = await process_message(
            telegram_id=telegram_id,
            user_text=user_text,
        )

        asyncio.create_task(update_user_interests(telegram_id, user_text))

        reply_markup = None
        if interactive_options:
            from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

            buttons = [
                [InlineKeyboardButton(text=opt["text"], callback_data=opt["callback_data"])]
                for opt in interactive_options
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await update_with_response(
            callback.message, thinking_msg, response_text, reply_markup=reply_markup
        )

    except Exception as e:
        logger.error("error_processing_callback", error=str(e), telegram_id=telegram_id)
        await send_error(callback.message, language=language)
