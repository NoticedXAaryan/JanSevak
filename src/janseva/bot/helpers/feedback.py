"""
Helper functions for standardizing bot UX feedback.
Includes typing indicators, thinking messages, error handling,
and Markdown → Telegram HTML conversion.
"""

import re

import structlog
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

logger = structlog.get_logger()


def markdown_to_telegram_html(text: str) -> str:
    """
    Convert common Markdown formatting to Telegram-compatible HTML.

    Telegram supports: <b>, <i>, <code>, <pre>, <a>, <s>, <u>
    Telegram does NOT support: headings, horizontal rules, tables, images
    """
    if not text:
        return text

    # Remove horizontal rules
    text = re.sub(r"^---+\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^___+\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\*\*\*+\s*$", "", text, flags=re.MULTILINE)

    # Convert headings (### heading → <b>heading</b> with newline)
    text = re.sub(r"^#{1,6}\s+(.+)$", r"<b>\1</b>", text, flags=re.MULTILINE)

    # Convert bold: **text** or __text__
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"__(.+?)__", r"<b>\1</b>", text)

    # Convert italic: *text* or _text_ (but not inside words like file_name)
    # Only match when surrounded by spaces or at start/end of line
    text = re.sub(r"(?<!\w)\*([^*\n]+?)\*(?!\w)", r"<i>\1</i>", text)
    text = re.sub(r"(?<!\w)_([^_\n]+?)_(?!\w)", r"<i>\1</i>", text)

    # Convert inline code: `code`
    text = re.sub(r"`([^`\n]+?)`", r"<code>\1</code>", text)

    # Convert code blocks: ```lang\ncode\n``` → <pre>code</pre>
    text = re.sub(r"```\w*\n(.*?)```", r"<pre>\1</pre>", text, flags=re.DOTALL)

    # Convert strikethrough: ~~text~~
    text = re.sub(r"~~(.+?)~~", r"<s>\1</s>", text)

    # Convert links: [text](url) → <a href="url">text</a>
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)

    # Clean up excessive blank lines (max 2 in a row)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


async def send_thinking(message: Message) -> Message | None:
    """
    Send a 'thinking' message to give the user immediate feedback.
    Returns the sent Message object so it can be edited later.
    """
    try:
        await message.chat.do(action="typing")

        thinking_text = "🤔 <b>सोच रहा हूँ... / Thinking...</b>"
        return await message.answer(thinking_text)
    except Exception as e:
        logger.error(
            "error_sending_thinking_msg",
            error=str(e),
            telegram_id=message.from_user.id if message.from_user else None,
        )
        return None


async def update_with_response(
    original_message: Message,
    thinking_message: Message | None,
    response_text: str,
    reply_markup=None,
) -> None:
    """
    Replace the 'thinking' message with the actual AI response.
    Converts Markdown to Telegram HTML before sending.
    If editing fails (e.g., message was deleted), send it as a new message.
    """
    # Convert LLM Markdown output to Telegram HTML
    response_text = markdown_to_telegram_html(response_text)

    if not thinking_message:
        # Fallback to just sending a new message if thinking_message wasn't created
        await original_message.answer(response_text, reply_markup=reply_markup)
        return

    try:
        # If response is too long, we might need to send it in chunks.
        # Telegram limit is 4096. Let's be safe and chunk at 4000.
        if len(response_text) <= 4000:
            await thinking_message.edit_text(response_text, reply_markup=reply_markup)
        else:
            # Edit the first chunk, then send the rest as new messages
            chunks = _split_html_safe(response_text, 4000)
            await thinking_message.edit_text(chunks[0])
            for i, chunk in enumerate(chunks[1:]):
                # Only attach markup to the final chunk
                markup = reply_markup if i == len(chunks) - 2 else None
                await original_message.answer(chunk, reply_markup=markup)

    except TelegramBadRequest as e:
        logger.warning("failed_to_edit_thinking_msg", error=str(e))
        # If we can't edit it, just send a new message
        try:
            await original_message.answer(response_text, reply_markup=reply_markup)
        except TelegramBadRequest:
            # If HTML is malformed, strip all tags and try plain text
            clean = re.sub(r"<[^>]+>", "", response_text)
            await original_message.answer(clean, reply_markup=reply_markup)

        # Try to delete the old thinking message if possible
        try:
            await thinking_message.delete()
        except TelegramBadRequest:
            pass
    except Exception as e:
        logger.error("error_updating_response", error=str(e))
        await original_message.answer(response_text, reply_markup=reply_markup)


def _split_html_safe(text: str, max_len: int) -> list[str]:
    """Split text into chunks at line boundaries to avoid breaking HTML tags."""
    chunks = []
    current = ""
    for line in text.split("\n"):
        if len(current) + len(line) + 1 > max_len and current:
            chunks.append(current)
            current = line
        else:
            current = current + "\n" + line if current else line
    if current:
        chunks.append(current)
    return chunks if chunks else [text]


async def send_error(message: Message, language: str = "hi") -> None:
    """Send a standardized error message based on the user's language."""
    if language == "en":
        error_text = (
            "⚠️ Something went wrong while processing your request. Please try again in a moment."
        )
    else:
        error_text = "⚠️ कुछ गड़बड़ हो गई। कृपया थोड़ी देर बाद दोबारा कोशिश करें।"

    await message.answer(error_text)
