from aiogram import Router, types
from aiogram.filters import Command
from bot.i18n.translator import t
from bot.infra.db import SessionLocal
from bot.repositories.user_repo import UserRepo

router = Router()


@router.message(Command("lang"))
async def cmd_lang(message: types.Message, lang: str) -> None:
    parts = (message.text or "").strip().split()
    if len(parts) == 1:
        await message.answer(
            "Current language: %s\nUsage: /lang ru | /lang en" % lang
        )
        return
    lang = parts[1].lower()
    if lang not in {"ru", "en"}:
        await message.answer("Unknown language. Use: ru or en")
        return
    async with SessionLocal() as session:
        repo = UserRepo(session)
        await repo.get_or_create(message.from_user.id, message.from_user.username)
        await repo.set_lang(message.from_user.id, lang)
    await message.answer("Language set to: %s" % lang)
