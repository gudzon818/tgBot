from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from bot.infra.db import SessionLocal
from bot.repositories.user_repo import UserRepo


class UserLocaleMiddleware(BaseMiddleware):
    def __init__(self, default_lang: str = "ru") -> None:
        self.default_lang = default_lang

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user_id = None
        username = None
        if isinstance(event, Message) and event.from_user:
            user_id = event.from_user.id
            username = event.from_user.username
        elif isinstance(event, CallbackQuery) and event.from_user:
            user_id = event.from_user.id
            username = event.from_user.username

        if user_id is not None:
            async with SessionLocal() as session:
                repo = UserRepo(session)
                # ensure user exists and get language
                await repo.get_or_create(user_id=user_id, username=username, default_lang=self.default_lang)
                lang = await repo.get_lang(user_id=user_id, default_lang=self.default_lang)
                data["lang"] = lang
        else:
            data["lang"] = self.default_lang

        return await handler(event, data)
