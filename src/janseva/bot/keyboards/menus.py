"""
Reusable inline and reply keyboards for the bot.
"""
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Main menu reply keyboard shown to users."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📋 सरकारी सेवाएं"),
                KeyboardButton(text="🚨 गुमनाम शिकायत"),
            ],
            [
                KeyboardButton(text="🏥 स्वास्थ्य सेवा"),
                KeyboardButton(text="🌾 किसान सेवा"),
            ],
            [
                KeyboardButton(text="❓ सहायता / Help"),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def language_selection_keyboard() -> InlineKeyboardMarkup:
    """Language selection inline keyboard."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="हिंदी", callback_data="lang:hi"),
                InlineKeyboardButton(text="English", callback_data="lang:en"),
            ],
            [
                InlineKeyboardButton(text="मराठी", callback_data="lang:mr"),
                InlineKeyboardButton(text="ગુજરાતી", callback_data="lang:gu"),
            ],
            [
                InlineKeyboardButton(text="தமிழ்", callback_data="lang:ta"),
                InlineKeyboardButton(text="తెలుగు", callback_data="lang:te"),
            ],
        ]
    )


def confirm_report_keyboard() -> InlineKeyboardMarkup:
    """Confirmation keyboard for anonymous reports."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ हाँ, भेजें / Yes, submit", callback_data="report:confirm"),
                InlineKeyboardButton(text="❌ रद्द करें / Cancel", callback_data="report:cancel"),
            ],
        ]
    )
