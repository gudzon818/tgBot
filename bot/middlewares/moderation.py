from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from bot.services.moderation import is_muted, is_banned


class ModerationMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = getattr(event, "from_user", None)
        if user is None:
            return await handler(event, data)
        uid = user.id
        # Block banned users for any events
        if await is_banned(uid):
            return
        # Ignore messages while muted (but allow callbacks)
        if isinstance(event, Message) and await is_muted(uid):
            return
        return await handler(event, data)
