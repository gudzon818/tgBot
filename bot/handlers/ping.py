import time
from aiogram import Router, types
from aiogram.filters import Command
from bot.i18n.translator import t

router = Router()


@router.message(Command("ping"))
async def cmd_ping(message: types.Message, lang: str) -> None:
    start = time.perf_counter()
    m = await message.answer("Pong!")
    elapsed_ms = int((time.perf_counter() - start) * 1000)
    await m.edit_text(t("ping_pong", lang, ms=elapsed_ms))
