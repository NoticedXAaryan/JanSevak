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
