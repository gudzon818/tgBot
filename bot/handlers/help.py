from aiogram import Router, types, F
from aiogram.filters import Command
from bot.i18n.translator import t
from bot.services.cache import cache_get, cache_set
from bot.core.settings import settings

router = Router()


@router.message(Command("help"))
async def cmd_help(message: types.Message, lang: str) -> None:
    # Версия кеша v2, чтобы не подтягивать старый help с админскими командами
    cache_key = f"help:v2:{lang}"
    text = await cache_get(cache_key)
    if text is None:
        text = t("help", lang)
        await cache_set(cache_key, text, ttl_seconds=300)
    await message.answer(text)


@router.message(F.text.in_([t("menu_help", "ru"), t("menu_help", "en")]))
async def on_menu_help(message: types.Message, lang: str) -> None:
    await cmd_help(message, lang)


@router.message(F.text.in_([t("menu_admin_help", "ru"), t("menu_admin_help", "en")]))
async def on_menu_admin_help(message: types.Message, lang: str) -> None:
    uid = message.from_user.id
    is_admin = False
    if settings.admin_ids:
        is_admin = uid in set(settings.admin_ids)
    elif settings.admin_id is not None:
        is_admin = uid == settings.admin_id

    if not is_admin:
        await message.answer(t("access_denied", lang))
        return

    await message.answer(t("help_admin", lang))
