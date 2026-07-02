# Guide 11: Notifications & Interest Profiling

## What This Does
Proactively notifies users about new government schemes, deadlines, and opportunities based on their interests and query history.

## Prerequisites
- Guide 03 completed (AI agent core)
- Guide 04 completed (knowledge base)
- ARQ worker running (for scheduled jobs)

---

## Features

1. **Interest Profiling** — Track what users ask about (agriculture, education, health, etc.)
2. **Scheme Alerts** — When a new scheme is added, notify eligible users
3. **Deadline Reminders** — Remind users about upcoming application deadlines
4. **Activity Updates** — Inform about new developments in their area

---

## Implementation Steps

### 1. Interest Tracker
- Every query updates the user's `interests` array in the users table
- Use LLM to extract topics from queries (e.g., "subsidy" → ["agriculture", "subsidy"])
- Track frequency to rank interests

### 2. Notification Engine
**File: `src/janseva/notifications/engine.py`**

```python
"""Notification dispatch engine."""
from janseva.db.engine import async_session_factory
from janseva.db.models.user import User
from sqlalchemy import select


async def find_users_by_interest(interest: str) -> list:
    """Find users whose interests match the given topic."""
    async with async_session_factory() as session:
        result = await session.execute(
            select(User).where(User.interests.contains([interest]))
        )
        return list(result.scalars().all())


async def send_notification(telegram_id: int, message: str, bot):
    """Send a notification message to a user via Telegram."""
    try:
        await bot.send_message(chat_id=telegram_id, text=message, parse_mode="HTML")
    except Exception:
        pass  # User may have blocked the bot
```

### 3. Scheduled Jobs (ARQ)
- Run daily: check for new schemes, upcoming deadlines
- Match against user interest profiles
- Send targeted notifications

### 4. User Preferences
- `/notifications on` / `/notifications off`
- Frequency settings: immediate, daily digest, weekly digest

---

## Git Checkpoint
```bash
git add -A
git commit -m "feat(notifications): implement interest profiling and notification engine"
```
