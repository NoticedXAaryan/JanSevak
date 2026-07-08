"""
Handles /start and /help commands.
/start — Registers new users, shows welcome message.
/help — Shows available features.
"""

import structlog
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy import select, update

from janseva.bot.helpers.constants import LANGUAGES
from janseva.db.engine import async_session_factory
from janseva.db.models.conversation import Conversation
from janseva.db.models.user import User

logger = structlog.get_logger()

start_router = Router(name="start")




def _get_language_keyboard() -> InlineKeyboardMarkup:
    """Generate a dynamic inline keyboard with all supported languages (3 per row)."""
    buttons = []
    current_row = []

    for code, (en_name, native_name) in LANGUAGES.items():
        text = f"{native_name}" if en_name == native_name else f"{native_name} ({en_name})"
        current_row.append(InlineKeyboardButton(text=text, callback_data=f"lang_{code}"))

        if len(current_row) == 3:
            buttons.append(current_row)
            current_row = []

    if current_row:
        buttons.append(current_row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


@start_router.message(CommandStart())
async def handle_start(message: Message) -> None:
    """
    Handle /start command.
    - If new user: create a record in the database.
    - If returning user: welcome them back.
    """
    if not message.from_user:
        return

    telegram_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username

    async with async_session_factory() as session:
        # Check if user already exists
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()

        if user is None:
            # New user — register them
            user = User(
                telegram_id=telegram_id,
                telegram_username=username,
                full_name=full_name,
                language="hi",  # Default until they choose
                onboarding_complete=False,
            )
            session.add(user)
            await session.commit()
            logger.info("new_user_registered", telegram_id=telegram_id, name=full_name)
        else:
            # Reset onboarding if they restart
            user.onboarding_complete = False
            session.add(user)
            await session.commit()
            logger.info("returning_user_restarted", telegram_id=telegram_id, name=full_name)

        keyboard = _get_language_keyboard()

        welcome_text = (
            f"🙏 <b>नमस्ते {full_name}! / Welcome!</b>\n\n"
            "मैं <b>जनसेवा (JanSeva)</b> हूँ — आपका AI सहायक। / I am JanSeva — your AI assistant.\n\n"
            "कृपया अपनी भाषा चुनें / Please select your language:"
        )

    await message.answer(welcome_text, reply_markup=keyboard)


@start_router.message(Command("language"))
async def handle_language_command(message: Message) -> None:
    """Handle /language command to change language."""
    keyboard = _get_language_keyboard()
    await message.answer(
        "कृपया अपनी नई भाषा चुनें / Please select your new language:", reply_markup=keyboard
    )


@start_router.message(Command("help"))
async def handle_help(message: Message) -> None:
    """Handle /help command — show available features in English + Hindi."""
    help_text = (
        "📖 <b>JanSeva — Help / सहायता</b>\n\n"
        "<b>Available Commands:</b>\n"
        "/start — Start or restart the bot\n"
        "/help — Show this help message\n"
        "/report — Submit an anonymous report (गुमनाम शिकायत)\n"
        "/language — Change your preferred language\n"
        "/status — Check the status of your reports or queries\n"
        "/notifications [on/off] — Toggle targeted scheme alerts\n\n"
        "<b>How to Use:</b>\n"
        "• Just type your question in Hindi or English\n"
        "• Send a voice note 🎙️ in any Indian language\n"
        "• Use /report for anonymous complaints\n\n"
        "<b>Examples:</b>\n"
        '• "आय प्रमाण पत्र के लिए क्या चाहिए?"\n'
        '• "What documents do I need for a caste certificate?"\n'
        '• "मेरे पास कौन-कौन सी सब्सिडी उपलब्ध हैं?"\n'
        '• "Find me an eye doctor nearby"\n\n'
        "<i>आपकी सभी बातचीत सुरक्षित है। गुमनाम रिपोर्ट में आपकी पहचान कभी साझा नहीं की जाती।</i>"
    )
    await message.answer(help_text)


@start_router.message(Command("notifications"))
async def handle_notifications_toggle(message: Message) -> None:
    """Handle /notifications on|off."""
    if not message.from_user:
        return

    telegram_id = message.from_user.id
    text = message.text.lower() if message.text else ""

    if "on" in text:
        enabled = True
    elif "off" in text:
        enabled = False
    else:
        await message.answer("Usage: /notifications on OR /notifications off")
        return

    async with async_session_factory() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if user:
            user.notifications_enabled = enabled
            await session.commit()

            if enabled:
                await message.answer(
                    "✅ Notifications turned ON. We will send you relevant scheme alerts."
                )
            else:
                await message.answer(
                    "🔕 Notifications turned OFF. You will no longer receive proactive alerts."
                )




@start_router.message(Command("reset"))
async def handle_reset(message: Message) -> None:
    """
    Handle /reset command.
    Soft-wipes user data for a fresh restart:
    - Closes active conversations
    - Clears preferences, location, and interests
    - Leaves historical records in the DB (for compliance)
    """
    if not message.from_user:
        return

    telegram_id = message.from_user.id

    async with async_session_factory() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()

        if not user:
            await message.answer("You are not registered yet. Send /start to begin.")
            return

        # 1. Close active conversations
        await session.execute(
            update(Conversation)
            .where(Conversation.user_id == user.id)
            .where(Conversation.status == "active")
            .values(status="completed")
        )

        # 2. Reset user profile data
        user.onboarding_complete = False
        user.language = "hi"
        user.district = None
        user.state = None
        user.interests = []

        await session.commit()
        logger.info("user_data_reset", telegram_id=telegram_id)

        # 3. Inform the user and trigger start flow
        await message.answer(
            "♻️ <b>आपका डेटा रीसेट कर दिया गया है। / Your data has been reset.</b>\nLet's start fresh!"
        )

        # Manually invoke the start handler to re-trigger onboarding
        await handle_start(message)
