"""
Handles voice messages.
Uses STT (Whisper) to transcribe, then passes to the AI Agent Pipeline.
"""

import os
import tempfile

import structlog
from aiogram import F, Router
from aiogram.types import Message

from janseva.agents.service import process_message
from janseva.voice.audio_utils import ogg_to_wav
from janseva.voice.stt import transcribe

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

    # Duration limit check
    if message.voice.duration > 120:
        await message.answer(
            "आपका वॉइस मैसेज बहुत लंबा है। कृपया इसे 2 मिनट (120 सेकंड) से छोटा रखें।\n"
            "Your voice message is too long. Please keep it under 2 minutes (120 seconds)."
        )
        return

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
        stt_result = await transcribe(wav_path)
        user_text = stt_result.get("text", "")

        # Whisper hallucination filter
        hallucinations = ["[silence]", "(silence)", "[music]", "(music)", "thank you.", "subtitles by", "amara.org", "blank_audio"]
        clean_text = user_text.lower().strip()
        for h in hallucinations:
            if clean_text == h or h in clean_text:
                # If the entire text is just a hallucination token
                if len(clean_text) < len(h) + 10:
                    user_text = ""
                    break

        if not user_text:
            await message.answer(
                "मुझे आपकी आवाज़ समझ नहीं आई या बैकग्राउंड में शोर था। कृपया दोबारा कोशिश करें।\nI couldn't understand your voice or there was background noise. Please try again."
            )
            return

        import asyncio

        from janseva.notifications.profiler import update_user_interests

        # 4. Process transcribed text via AI Agent
        await message.chat.do(action="typing")
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

        # 5. Send response
        if len(response_text) <= 4096:
            await message.answer(response_text, reply_markup=reply_markup)
        else:
            for i in range(0, len(response_text), 4096):
                if i + 4096 >= len(response_text):
                    await message.answer(response_text[i : i + 4096], reply_markup=reply_markup)
                else:
                    await message.answer(response_text[i : i + 4096])

    except Exception as e:
        logger.error("voice_processing_failed", error=str(e))
        await message.answer(
            "आपके वॉइस मैसेज को प्रोसेस करने में कुछ समस्या आई।\nThere was an issue processing your voice message."
        )
    finally:
        # Cleanup temp files
        if os.path.exists(ogg_path):
            os.remove(ogg_path)
        if wav_path and os.path.exists(wav_path):
            os.remove(wav_path)
