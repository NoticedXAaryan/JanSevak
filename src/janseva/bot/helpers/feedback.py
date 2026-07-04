"""
Helper functions for standardizing bot UX feedback.
Includes typing indicators, thinking messages, and error handling.
"""
import structlog
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

logger = structlog.get_logger()

async def send_thinking(message: Message) -> Message | None:
    """
    Send a 'thinking' message to give the user immediate feedback.
    Returns the sent Message object so it can be edited later.
    """
    try:
        await message.chat.do(action="typing")
        
        thinking_text = (
            "🤔 <b>सोच रहा हूँ... / Thinking...</b>"
        )
        return await message.answer(thinking_text)
    except Exception as e:
        logger.error("error_sending_thinking_msg", error=str(e), telegram_id=message.from_user.id if message.from_user else None)
        return None

async def update_with_response(original_message: Message, thinking_message: Message | None, response_text: str) -> None:
    """
    Replace the 'thinking' message with the actual AI response.
    If editing fails (e.g., message was deleted), send it as a new message.
    """
    if not thinking_message:
        # Fallback to just sending a new message if thinking_message wasn't created
        await original_message.answer(response_text)
        return

    try:
        # If response is too long, we might need to send it in chunks.
        # Telegram limit is 4096. Let's be safe and chunk at 4000.
        if len(response_text) <= 4000:
            await thinking_message.edit_text(response_text)
        else:
            # Edit the first chunk, then send the rest as new messages
            chunks = [response_text[i:i + 4000] for i in range(0, len(response_text), 4000)]
            await thinking_message.edit_text(chunks[0])
            for chunk in chunks[1:]:
                await original_message.answer(chunk)
                
    except TelegramBadRequest as e:
        logger.warning("failed_to_edit_thinking_msg", error=str(e))
        # If we can't edit it, just send a new message
        await original_message.answer(response_text)
        
        # Try to delete the old thinking message if possible
        try:
            await thinking_message.delete()
        except TelegramBadRequest:
            pass
    except Exception as e:
        logger.error("error_updating_response", error=str(e))
        await original_message.answer(response_text)

async def send_error(message: Message, language: str = "hi") -> None:
    """Send a standardized error message based on the user's language."""
    if language == "en":
        error_text = "⚠️ Something went wrong while processing your request. Please try again in a moment."
    else:
        error_text = "⚠️ कुछ गड़बड़ हो गई। कृपया थोड़ी देर बाद दोबारा कोशिश करें।"
        
    await message.answer(error_text)
