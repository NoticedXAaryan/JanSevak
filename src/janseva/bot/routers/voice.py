"""
Handles voice messages.
Uses STT (Whisper) to transcribe, then passes to the AI Agent Pipeline.
"""
import os
import tempfile
import structlog
from aiogram import Router, F
from aiogram.types import Message

from janseva.voice.audio_utils import ogg_to_wav
from janseva.voice.stt import transcribe
from janseva.agents.service import process_message

logger = structlog.get_logger()

voice_router = Router(name="voice")


@voice_router.message(F.voice)
async def handle_voice_message(message: Message) -> None:
    """
    Handle incoming voice messages.
    STT → AI Agent → Text Response.
    """
    if not message.from_user or not message.voice or not message.bot:
        return

    telegram_id = message.from_user.id
    logger.info(
        "voice_message_received",
        telegram_id=telegram_id,
        duration_seconds=message.voice.duration,
    )

    # Indicate processing
    await message.chat.do(action="record_voice")

    ogg_path = tempfile.mktemp(suffix=".ogg")
    wav_path = None
    
    try:
        # 1. Download voice file
        await message.bot.download(message.voice, destination=ogg_path)
        
        # 2. Convert to WAV for Whisper
        wav_path = ogg_to_wav(ogg_path)
        
        # 3. Transcribe to Text
        stt_result = transcribe(wav_path)
        user_text = stt_result.get("text", "")
        
        if not user_text:
            await message.answer("मुझे आपकी आवाज़ समझ नहीं आई। कृपया दोबारा कोशिश करें।\nI couldn't understand your voice. Please try again.")
            return

        # 4. Process transcribed text via AI Agent
        await message.chat.do(action="typing")
        response = await process_message(
            telegram_id=telegram_id,
            user_text=user_text,
        )

        # 5. Send response
        if len(response) <= 4096:
            await message.answer(response)
        else:
            for i in range(0, len(response), 4096):
                await message.answer(response[i:i + 4096])

    except Exception as e:
        logger.error("voice_processing_failed", error=str(e))
        await message.answer("आपके वॉइस मैसेज को प्रोसेस करने में कुछ समस्या आई।\nThere was an issue processing your voice message.")
    finally:
        # Cleanup temp files
        if os.path.exists(ogg_path):
            os.remove(ogg_path)
        if wav_path and os.path.exists(wav_path):
            os.remove(wav_path)
