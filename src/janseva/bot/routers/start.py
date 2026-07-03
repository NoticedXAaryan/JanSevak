"""
Handles /start and /help commands.
/start — Registers new users, shows welcome message.
/help — Shows available features.
"""
import structlog
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from janseva.db.engine import async_session_factory
from janseva.db.models.user import User

from sqlalchemy import select

logger = structlog.get_logger()

start_router = Router(name="start")


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
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            # New user — register them
            user = User(
                telegram_id=telegram_id,
                telegram_username=username,
                full_name=full_name,
                language="hi",  # Default to Hindi
            )
            session.add(user)
            await session.commit()
            logger.info("new_user_registered", telegram_id=telegram_id, name=full_name)

            welcome_text = (
                f"🙏 <b>नमस्ते {full_name}!</b>\n\n"
                "मैं <b>जनसेवा (JanSeva)</b> हूँ — आपका AI सहायक।\n\n"
                "मैं इन सेवाओं में आपकी मदद कर सकता/सकती हूँ:\n\n"
                "📋 <b>सरकारी सेवाएं</b> — आय प्रमाण पत्र, जाति प्रमाण पत्र, भूमि रिकॉर्ड\n"
                "🚨 <b>गुमनाम शिकायत</b> — भ्रष्टाचार या गलत काम की सुरक्षित रिपोर्ट\n"
                "🏥 <b>स्वास्थ्य सेवाएं</b> — अस्पताल खोजें, अपॉइंटमेंट बुक करें\n"
                "🌾 <b>किसान सेवाएं</b> — सब्सिडी, मंडी भाव, लॉजिस्टिक्स\n\n"
                "बस अपना सवाल हिंदी या अंग्रेजी में लिखें, या वॉइस मैसेज भेजें! 🎙️\n\n"
                "<i>Type /help for English instructions.</i>"
            )
        else:
            logger.info("returning_user", telegram_id=telegram_id, name=full_name)
            welcome_text = (
                f"🙏 <b>वापसी पर स्वागत है, {full_name}!</b>\n\n"
                "आप कैसे हैं? आज मैं आपकी क्या मदद कर सकता/सकती हूँ?\n\n"
                "<i>Type /help to see available commands.</i>"
            )

    await message.answer(welcome_text)


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
        "• \"आय प्रमाण पत्र के लिए क्या चाहिए?\"\n"
        "• \"What documents do I need for a caste certificate?\"\n"
        "• \"मेरे पास कौन-कौन सी सब्सिडी उपलब्ध हैं?\"\n"
        "• \"Find me an eye doctor nearby\"\n\n"
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
                await message.answer("✅ Notifications turned ON. We will send you relevant scheme alerts.")
            else:
                await message.answer("🔕 Notifications turned OFF. You will no longer receive proactive alerts.")
