from aiogram import Router, types
from aiogram.filters import Command
from bot.i18n.translator import t
from bot.services.cache import cache_get, cache_set

router = Router()


@router.message(Command("help"))
async def cmd_help(message: types.Message, lang: str) -> None:
    cache_key = f"help:{lang}"
    text = await cache_get(cache_key)
    if text is None:
        text = t("help", lang)
        await cache_set(cache_key, text, ttl_seconds=300)
    await message.answer(text)
