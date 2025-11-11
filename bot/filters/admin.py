from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.core.settings import settings


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return settings.admin_id is not None and message.from_user and message.from_user.id == settings.admin_id
