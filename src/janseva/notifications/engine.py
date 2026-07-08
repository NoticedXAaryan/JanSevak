"""Notification dispatch engine."""

import logging

from aiogram import Bot
from sqlalchemy import select

from janseva.db.engine import async_session_factory
from janseva.db.models.user import User

logger = logging.getLogger(__name__)


async def find_users_by_interest(interest: str) -> list[User]:
    """Find users who have notifications enabled and matching interest."""
    async with async_session_factory() as session:
        # User.interests is an ARRAY(Text)
        stmt = select(User).where(
            User.notifications_enabled,
            User.is_active,
            User.interests.any(interest),  # Postgres specific array operator
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())


async def get_all_opted_in_users() -> list[User]:
    """Find all users who have notifications enabled."""
    async with async_session_factory() as session:
        stmt = select(User).where(User.notifications_enabled, User.is_active)
        result = await session.execute(stmt)
        return list(result.scalars().all())


async def send_notification(telegram_id: int, message: str, bot: Bot) -> bool:
    """Send a notification message to a user via Telegram."""
    try:
        await bot.send_message(chat_id=telegram_id, text=message, parse_mode="HTML")
        return True
    except Exception as e:
        logger.warning(f"Failed to send notification to {telegram_id}: {e}")
        return False


async def broadcast_scheme_alert(scheme_data: dict, bot: Bot):
    """
    Broadcast a new scheme to relevant users.
    scheme_data should contain 'title', 'description', 'interest_tag'
    """
    interest_tag = scheme_data.get("interest_tag")
    if interest_tag:
        target_users = await find_users_by_interest(interest_tag)
    else:
        target_users = await get_all_opted_in_users()

    logger.info(f"Broadcasting scheme '{scheme_data.get('title')}' to {len(target_users)} users.")

    message = f"📢 <b>New Update: {scheme_data.get('title', 'Scheme Alert')}</b>\n\n"
    message += f"{scheme_data.get('description', '')}\n\n"
    message += "<i>You are receiving this based on your previous queries. To turn off notifications, send /notifications off</i>"

    success_count = 0
    for user in target_users:
        if await send_notification(user.telegram_id, message, bot):
            success_count += 1

    logger.info(f"Successfully broadcasted to {success_count}/{len(target_users)} users.")
