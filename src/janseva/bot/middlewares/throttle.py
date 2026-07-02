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
