from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from bot.core.settings import settings


class IsAdmin(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        user = getattr(event, "from_user", None)
        if not user:
            return False
        uid = user.id
        # Support both single ADMIN_ID and list ADMIN_IDS
        if settings.admin_ids:
            return uid in set(settings.admin_ids)
        if settings.admin_id is not None:
            return uid == settings.admin_id
        return False
