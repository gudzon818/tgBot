from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from redis.asyncio import Redis


class RedisRateLimitMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis, key_prefix: str = "rl", window_seconds: float = 1.5) -> None:
        self.redis = redis
        self.key_prefix = key_prefix
        self.window = window_seconds

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Message) and event.from_user:
            key = f"{self.key_prefix}:user:{event.from_user.id}"
            try:
                val = await self.redis.incr(key)
                if val == 1:
                    await self.redis.expire(key, int(self.window))
                else:
                    return
            except Exception:
                pass
        return await handler(event, data)
