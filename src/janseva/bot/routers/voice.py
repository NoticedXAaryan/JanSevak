"""
Handles voice messages.
Phase 1: Acknowledge receipt.
Phase 3: Full STT → Agent → TTS pipeline (Guide 08).
"""
import structlog
from aiogram import Router, F
from aiogram.types import Message

logger = structlog.get_logger()

voice_router = Router(name="voice")


@voice_router.message(F.voice)
async def handle_voice_message(message: Message) -> None:
    """
    Handle incoming voice messages.

    Phase 1: Acknowledge receipt (placeholder).
    Phase 3: STT → AI Agent → TTS pipeline.
    """
    if not message.from_user:
        return

    logger.info(
        "voice_message_received",
        telegram_id=message.from_user.id,
        duration_seconds=message.voice.duration if message.voice else 0,
    )

    await message.answer(
        "🎙️ <b>वॉइस मैसेज प्राप्त हुआ!</b>\n\n"
        "वॉइस सपोर्ट जल्द ही आ रहा है। "
        "कृपया अभी के लिए अपना सवाल टाइप करें।\n\n"
        "<i>Voice support coming soon. Please type your question for now.</i>"
    )
