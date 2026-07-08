"""
Handles the guided onboarding flow (language and district selection).
"""

import structlog
from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import select

from janseva.bot.helpers.constants import INDIA_DISTRICTS
from janseva.db.engine import async_session_factory
from janseva.db.models.user import User

logger = structlog.get_logger()

onboarding_router = Router(name="onboarding")



@onboarding_router.callback_query(F.data.startswith("lang_"))
async def handle_language_selection(callback: CallbackQuery):
    """Save selected language and prompt for state selection."""
    if not callback.message or not callback.from_user:
        return

    lang_code = callback.data.split("_")[1]
    telegram_id = callback.from_user.id

    # Text in both languages since we just selected one
    msg_texts = {
        "hi": ("आपने हिंदी चुनी है। ✅\n\nअब कृपया अपना राज्य (State) चुनें:", "कृपया चुनें / Please select"),
        "en": (
            "You have selected English. ✅\n\nNow please select your State:",
            "Please select / कृपया चुनें",
        ),
    }

    # Fallback for other languages (using English structure with localized names from DB ideally, but here we keep it simple)
    text = msg_texts.get(lang_code, msg_texts["en"])[0]

    if lang_code not in msg_texts and lang_code != "en":
        text = "Language selected. ✅\n\nNow please select your State (राज्य चुनें):"

    async with async_session_factory() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()

        if user:
            user.language = lang_code
            await session.commit()

    # Show state keyboard (2 per row)
    buttons = []
    current_row = []
    for state_name in INDIA_DISTRICTS.keys():
        # Truncate if too long, though they are mostly fine
        btn_text = state_name[:20]
        current_row.append(InlineKeyboardButton(text=btn_text, callback_data=f"state_{state_name}"))
        if len(current_row) == 2:
            buttons.append(current_row)
            current_row = []
    if current_row:
        buttons.append(current_row)

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@onboarding_router.callback_query(F.data.startswith("state_"))
async def handle_state_selection(callback: CallbackQuery):
    """Show districts for the selected state."""
    if not callback.message or not callback.from_user:
        return

    state_name = callback.data.split("_", 1)[1]

    # Show district keyboard for this state
    districts = INDIA_DISTRICTS.get(state_name, ["Other"])
    buttons = []
    current_row = []
    for dist in districts:
        current_row.append(InlineKeyboardButton(text=dist, callback_data=f"dist_{dist}"))
        if len(current_row) == 2:
            buttons.append(current_row)
            current_row = []
    if current_row:
        buttons.append(current_row)

    # Add a back button
    buttons.append(
        [InlineKeyboardButton(text="⬅️ Back to States", callback_data="lang_en")]
    )  # hack to just reload states in EN

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    text = f"State: {state_name} ✅\n\nNow please select your District (जिला चुनें):"
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@onboarding_router.callback_query(F.data.startswith("dist_"))
async def handle_district_selection(callback: CallbackQuery):
    """Save selected district, mark onboarding complete, and show welcome."""
    if not callback.message or not callback.from_user:
        return

    district = callback.data.split("_", 1)[1]
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
