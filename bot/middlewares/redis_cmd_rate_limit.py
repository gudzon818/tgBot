from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
import redis.asyncio as aioredis


class RedisCommandRateLimitMiddleware(BaseMiddleware):
    def __init__(self, redis: aioredis.Redis, windows: Dict[str, int] | None = None, default_window: int = 0) -> None:
        self.redis = redis
        self.windows = windows or {}
        self.default = default_window

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Message) and event.text and event.text.startswith("/") and event.from_user:
            cmd = event.text.split()[0]
            win = int(self.windows.get(cmd, self.default))
            if win > 0:
                key = f"rl:{event.from_user.id}:{cmd}"
                try:
                    n = await self.redis.incr(key)
                    if n == 1:
                        await self.redis.expire(key, win)
                    if n > 1:
                        return  # over limit — drop silently
                except Exception:
                    # If Redis fails, proceed without dropping
                    pass
        return await handler(event, data)
