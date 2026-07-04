"""
Handles the guided onboarding flow (language and district selection).
"""
import structlog
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from janseva.db.engine import async_session_factory
from janseva.db.models.user import User
from sqlalchemy import select

logger = structlog.get_logger()

onboarding_router = Router(name="onboarding")

@onboarding_router.callback_query(F.data.startswith("lang_"))
async def handle_language_selection(callback: CallbackQuery):
    """Save selected language and prompt for district."""
    if not callback.message or not callback.from_user:
        return

    lang_code = callback.data.split("_")[1]
    telegram_id = callback.from_user.id
    
    # Text in both languages since we just selected one
    msg_texts = {
        "hi": ("आपने हिंदी चुनी है। ✅\n\nअब कृपया अपना जिला (District) चुनें:", "कृपया चुनें / Please select"),
        "en": ("You have selected English. ✅\n\nNow please select your District:", "Please select / कृपया चुनें")
    }
    
    text, prompt = msg_texts.get(lang_code, msg_texts["hi"])

    async with async_session_factory() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        
        if user:
            user.language = lang_code
            await session.commit()
            
    # Show district keyboard (hardcoded common ones for now, ideally fetched from DB)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Indore (इंदौर)", callback_data="dist_indore"),
            InlineKeyboardButton(text="Bhopal (भोपाल)", callback_data="dist_bhopal")
        ],
        [
            InlineKeyboardButton(text="Ujjain (उज्जैन)", callback_data="dist_ujjain"),
            InlineKeyboardButton(text="Other (अन्य)", callback_data="dist_other")
        ]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@onboarding_router.callback_query(F.data.startswith("dist_"))
async def handle_district_selection(callback: CallbackQuery):
    """Save selected district, mark onboarding complete, and show welcome."""
    if not callback.message or not callback.from_user:
        return

    district = callback.data.split("_")[1]
    telegram_id = callback.from_user.id
    
    async with async_session_factory() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        
        if user:
            user.district = district
            user.onboarding_complete = True
            await session.commit()
            
            # Show customized welcome message based on language
            if user.language == "en":
                welcome_text = (
                    f"🎉 <b>Onboarding Complete!</b>\n\n"
                    f"Welcome to JanSeva, {user.full_name or 'friend'}!\n\n"
                    f"You can now ask me about:\n"
                    f"📄 Government documents & certificates\n"
                    f"🏥 Nearby hospitals and healthcare\n"
                    f"🌾 Farmer schemes and mandi prices\n"
                    f"🚨 Anonymous corruption reporting\n\n"
                    f"<i>Just type your question or send a voice note to begin!</i>"
                )
            else:
                welcome_text = (
                    f"🎉 <b>रजिस्ट्रेशन पूरा हुआ!</b>\n\n"
                    f"जनसेवा में आपका स्वागत है, {user.full_name or 'दोस्त'}!\n\n"
                    f"अब आप मुझसे पूछ सकते हैं:\n"
                    f"📄 सरकारी दस्तावेज़ और प्रमाण पत्र\n"
                    f"🏥 नजदीकी अस्पताल और स्वास्थ्य सेवाएं\n"
                    f"🌾 किसान योजनाएं और मंडी भाव\n"
                    f"🚨 गुमनाम भ्रष्टाचार की शिकायत\n\n"
                    f"<i>शुरू करने के लिए बस अपना सवाल टाइप करें या वॉइस नोट भेजें!</i>"
                )
                
            await callback.message.edit_text(welcome_text)
            await callback.answer()
