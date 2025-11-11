import time
from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, limit_seconds: float = 1.5) -> None:
        self.limit = limit_seconds
        self._last_time: Dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Message) and event.from_user:
            now = time.monotonic()
            user_id = event.from_user.id
            last = self._last_time.get(user_id, 0.0)
            if now - last < self.limit:
                return
            self._last_time[user_id] = now
        return await handler(event, data)
