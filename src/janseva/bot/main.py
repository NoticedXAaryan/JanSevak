"""
JanSeva Telegram Bot — Entry Point.

This module initializes the aiogram bot, registers all routers,
sets up middlewares, and starts polling for messages.

Run with: uv run python -m janseva.bot.main
"""
import asyncio
import structlog

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from janseva.config import settings
from janseva.common.logging import setup_logging
from janseva.bot.routers.start import start_router
from janseva.bot.routers.text import text_router
from janseva.bot.routers.voice import voice_router
from janseva.bot.middlewares.session import DatabaseSessionMiddleware
from janseva.bot.middlewares.throttle import ThrottleMiddleware

logger = structlog.get_logger()


async def main() -> None:
    """Initialize and start the bot."""
    # Set up structured logging
    setup_logging()
    logger.info("starting_bot", env=settings.env)

    # Create bot instance
    bot = Bot(
        token=settings.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # Create dispatcher (handles all incoming updates)
    dp = Dispatcher()

    # Register middlewares (order matters — first registered = first executed)
    dp.message.middleware(ThrottleMiddleware(rate_limit=1.0))  # 1 msg/sec per user
    dp.message.middleware(DatabaseSessionMiddleware())

    # Register routers (order matters — first match wins)
    dp.include_router(start_router)   # /start, /help commands
    dp.include_router(voice_router)   # Voice messages (before text, so voice isn't caught by text handler)
    dp.include_router(text_router)    # Text messages (catch-all)

    # Start polling
    logger.info("bot_started", bot_username=(await bot.me()).username)
    try:
        await dp.start_polling(bot, allowed_updates=["message", "callback_query"])
    finally:
        await bot.session.close()
        logger.info("bot_stopped")


if __name__ == "__main__":
    asyncio.run(main())
