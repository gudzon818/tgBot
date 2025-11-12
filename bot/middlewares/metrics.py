import time
from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from bot.services.metrics import inc_update, inc_command, add_latency


class MetricsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        inc_update()
        cmd: str | None = None
        if isinstance(event, Message) and event.text:
            text = event.text.strip()
            if text.startswith("/"):
                cmd = text.split()[0]
        elif isinstance(event, CallbackQuery):
            cmd = "callback"

        if cmd:
            start = time.perf_counter()
            try:
                return await handler(event, data)
            finally:
                elapsed_ms = (time.perf_counter() - start) * 1000.0
                inc_command(cmd)
                add_latency(cmd, elapsed_ms)
        else:
            return await handler(event, data)
