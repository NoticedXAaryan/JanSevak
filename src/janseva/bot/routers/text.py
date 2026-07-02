"""
Handles all text messages that are not commands.
Forwards messages to the LangGraph agent pipeline and returns the response.
"""
import structlog
from aiogram import Router, F
from aiogram.types import Message

from janseva.agents.service import process_message

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

    # Show "typing" indicator while AI processes
    await message.chat.do(action="typing")

    # Process through AI agent pipeline
    response = await process_message(
        telegram_id=telegram_id,
        user_text=user_text,
    )

    # Send response (split if too long for Telegram's 4096 char limit)
    if len(response) <= 4096:
        await message.answer(response)
    else:
        # Split into chunks
        for i in range(0, len(response), 4096):
            chunk = response[i:i + 4096]
            await message.answer(chunk)
