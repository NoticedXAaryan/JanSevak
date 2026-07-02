"""
Handles all text messages that are not commands.
This is the main entry point for user queries.
In Phase 1, this echoes the message. Once the AI agent layer is built (Guide 03),
this will forward messages to the LangGraph orchestrator.
"""
import structlog
from aiogram import Router, F
from aiogram.types import Message

logger = structlog.get_logger()

text_router = Router(name="text")


@text_router.message(F.text)
async def handle_text_message(message: Message) -> None:
    """
    Handle incoming text messages.

    Phase 1: Echo the message back (placeholder).
    Phase 2: Forward to LangGraph orchestrator agent.
    """
    if not message.text or not message.from_user:
        return

    user_text = message.text.strip()
    telegram_id = message.from_user.id

    logger.info(
        "text_message_received",
        telegram_id=telegram_id,
        text_length=len(user_text),
    )

    # --- PHASE 1: Echo placeholder ---
    # TODO(guide-03): Replace with agent orchestrator call
    response = (
        f"📩 आपका सवाल मिल गया:\n\n"
        f"<i>\"{user_text}\"</i>\n\n"
        f"🔄 जनसेवा AI इस पर काम कर रहा है...\n"
        f"<i>(AI agent integration coming in Guide 03)</i>"
    )

    await message.answer(response)
