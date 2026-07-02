# Guide 02: Telegram Bot (aiogram 3.x)

## What This Does
Builds the Telegram bot layer using aiogram 3.x — the async interface through which citizens interact with JanSeva. This guide covers the bot entry point, command handlers, message routing, session middleware, and rate limiting.

## Prerequisites
- Guide 01 completed (project scaffolded, Docker services running, DB migrated)
- A Telegram bot token from @BotFather
- `TELEGRAM_BOT_TOKEN` set in `.env`

---

## How to Get a Telegram Bot Token

1. Open Telegram, search for `@BotFather`
2. Send `/newbot`
3. Choose a name (e.g., "JanSeva Bot")
4. Choose a username (e.g., `janseva_dev_bot` — must end in `bot`)
5. BotFather gives you a token like `7123456789:AAF...` — put this in `.env`

---

## Files to Create

### 1. Bot Entry Point

**File: `src/janseva/bot/main.py`**

```python
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
```

---

### 2. Start & Help Commands Router

**File: `src/janseva/bot/routers/start.py`**

```python
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
        "/status — Check the status of your reports or queries\n\n"
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
```

---

### 3. Text Message Handler

**File: `src/janseva/bot/routers/text.py`**

```python
"""
Handles all text messages that are not commands.
This is the main entry point for user queries.
In Phase 1, this echoes the message. Once the AI agent layer is built (Guide 03),
this will forward messages to the LangGraph orchestrator.
"""
import structlog
from aiogram import Router, F
from aiogram.types import Message

logger = structlog.get_logger()

text_router = Router(name="text")


@text_router.message(F.text)
async def handle_text_message(message: Message) -> None:
    """
    Handle incoming text messages.

    Phase 1: Echo the message back (placeholder).
    Phase 2: Forward to LangGraph orchestrator agent.
    """
    if not message.text or not message.from_user:
        return

    user_text = message.text.strip()
    telegram_id = message.from_user.id

    logger.info(
        "text_message_received",
        telegram_id=telegram_id,
        text_length=len(user_text),
    )

    # --- PHASE 1: Echo placeholder ---
    # TODO(guide-03): Replace with agent orchestrator call
    response = (
        f"📩 आपका सवाल मिल गया:\n\n"
        f"<i>\"{user_text}\"</i>\n\n"
        f"🔄 जनसेवा AI इस पर काम कर रहा है...\n"
        f"<i>(AI agent integration coming in Guide 03)</i>"
    )

    await message.answer(response)
```

---

### 4. Voice Message Handler (Stub)

**File: `src/janseva/bot/routers/voice.py`**

```python
"""
Handles voice messages.
Phase 1: Acknowledge receipt.
Phase 3: Full STT → Agent → TTS pipeline (Guide 08).
"""
import structlog
from aiogram import Router, F
from aiogram.types import Message

logger = structlog.get_logger()

voice_router = Router(name="voice")


@voice_router.message(F.voice)
async def handle_voice_message(message: Message) -> None:
    """
    Handle incoming voice messages.

    Phase 1: Acknowledge receipt (placeholder).
    Phase 3: STT → AI Agent → TTS pipeline.
    """
    if not message.from_user:
        return

    logger.info(
        "voice_message_received",
        telegram_id=message.from_user.id,
        duration_seconds=message.voice.duration if message.voice else 0,
    )

    await message.answer(
        "🎙️ <b>वॉइस मैसेज प्राप्त हुआ!</b>\n\n"
        "वॉइस सपोर्ट जल्द ही आ रहा है। "
        "कृपया अभी के लिए अपना सवाल टाइप करें।\n\n"
        "<i>Voice support coming soon. Please type your question for now.</i>"
    )
```

---

### 5. Database Session Middleware

**File: `src/janseva/bot/middlewares/session.py`**

```python
"""
Middleware that provides a database session to every handler.
The session is available in handler kwargs as 'db_session'.
"""
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from janseva.db.engine import async_session_factory


class DatabaseSessionMiddleware(BaseMiddleware):
    """Injects an async database session into every message handler."""

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        async with async_session_factory() as session:
            data["db_session"] = session
            return await handler(event, data)
```

---

### 6. Rate Limiting Middleware

**File: `src/janseva/bot/middlewares/throttle.py`**

```python
"""
Simple per-user rate limiting middleware.
Prevents users from overwhelming the bot with rapid messages.
"""
import time
from typing import Any, Awaitable, Callable, Dict

import structlog
from aiogram import BaseMiddleware
from aiogram.types import Message

logger = structlog.get_logger()


class ThrottleMiddleware(BaseMiddleware):
    """
    Per-user rate limiter.
    If a user sends messages faster than `rate_limit` seconds apart,
    the excess messages are silently dropped.
    """

    def __init__(self, rate_limit: float = 1.0) -> None:
        self.rate_limit = rate_limit
        self._user_timestamps: Dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not event.from_user:
            return await handler(event, data)

        user_id = event.from_user.id
        now = time.monotonic()
        last_time = self._user_timestamps.get(user_id, 0.0)

        if now - last_time < self.rate_limit:
            logger.debug("throttled_message", telegram_id=user_id)
            return  # Silently drop the message

        self._user_timestamps[user_id] = now
        return await handler(event, data)
```

---

### 7. Keyboard Builders (Menus)

**File: `src/janseva/bot/keyboards/menus.py`**

```python
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
```

---

### 8. Make the Bot Runnable as a Module

**File: `src/janseva/bot/__init__.py`** (update existing empty file)

```python
"""JanSeva Telegram Bot package."""
```

Add a `__main__.py` so the bot can be run with `python -m janseva.bot`:

**File: `src/janseva/bot/__main__.py`**

```python
"""Allow running the bot as: python -m janseva.bot"""
from janseva.bot.main import main
import asyncio

asyncio.run(main())
```

---

## Running the Bot

```bash
# Make sure Docker services are running
docker compose up -d

# Start the bot (from the GoogleXParul directory)
uv run python -m janseva.bot.main

# Or equivalently:
# uv run python -m janseva.bot
```

You should see:
```
starting_bot env=development
bot_started bot_username=janseva_dev_bot
```

---

## Verification Checklist

- [ ] Bot starts without errors
- [ ] Sending `/start` to the bot registers you and shows Hindi welcome message
- [ ] Sending `/start` again shows "welcome back" message
- [ ] Sending `/help` shows the help text
- [ ] Sending a text message shows the echo response
- [ ] Sending a voice note shows "coming soon" message
- [ ] Rapid messages (faster than 1/sec) are silently throttled
- [ ] Check PostgreSQL: a new row exists in the `users` table with your telegram_id

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `TelegramBadRequest: chat not found` | Make sure you've started a conversation with the bot first (click Start) |
| `aiogram.exceptions.TelegramUnauthorizedError` | Your bot token is wrong. Check `.env` |
| Bot doesn't respond | Check terminal for errors. Common: database connection failed (Docker not running) |
| `ModuleNotFoundError` | Run from the `GoogleXParul` directory, ensure `uv sync` was run |

---

## Git Checkpoint

```bash
git add -A
git commit -m "feat(bot): implement Telegram bot with aiogram 3.x

- /start command with user registration and Hindi welcome
- /help command with bilingual instructions
- Text message handler (echo placeholder for agent integration)
- Voice message handler (acknowledgment placeholder)
- Database session middleware
- Per-user rate limiting middleware (1 msg/sec)
- Reply keyboards: main menu, language selection, report confirmation
- Bot runnable as python -m janseva.bot"
```
