from aiogram import Router, types
from aiogram.filters import Command
from bot.i18n.translator import t

router = Router()


@router.message(Command("health"))
async def cmd_health(message: types.Message, lang: str) -> None:
    await message.answer(t("health_ok", lang))
