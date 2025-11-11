from aiogram import Router, types
from aiogram.filters import Command
from bot.i18n.translator import set_user_lang, get_user_lang

router = Router()


@router.message(Command("lang"))
async def cmd_lang(message: types.Message) -> None:
    parts = (message.text or "").strip().split()
    if len(parts) == 1:
        cur = get_user_lang(message.from_user.id)
        await message.answer(
            "Current language: %s\nUsage: /lang ru | /lang en" % cur
        )
        return
    lang = parts[1].lower()
    if lang not in {"ru", "en"}:
        await message.answer("Unknown language. Use: ru or en")
        return
    set_user_lang(message.from_user.id, lang)
    await message.answer("Language set to: %s" % lang)
