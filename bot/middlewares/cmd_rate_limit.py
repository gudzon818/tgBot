from typing import Any, Callable, Dict, Awaitable
import time
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

# Simple in-memory per-user per-command window limiter
_last_seen: Dict[tuple[int, str], float] = {}


class CommandRateLimitMiddleware(BaseMiddleware):
    def __init__(self, windows: Dict[str, float] | None = None, default_window: float = 0.0) -> None:
        # windows like {"/ping": 1.0, "/feedback": 10.0}
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
            win = self.windows.get(cmd, self.default)
            if win > 0:
                key = (event.from_user.id, cmd)
                now = time.monotonic()
                last = _last_seen.get(key, 0.0)
                if now - last < win:
                    return  # drop silently
                _last_seen[key] = now
        return await handler(event, data)
