from aiogram import Router, types
from aiogram.filters import CommandStart
from bot.keyboards.main import main_menu
from bot.keyboards.inline import like_dislike_kb
from bot.i18n.translator import t, get_user_lang

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    lang = get_user_lang(message.from_user.id)
    await message.answer(t("start_greeting", lang), reply_markup=main_menu())
    await message.answer(t("rate_prompt", lang), reply_markup=like_dislike_kb(lang))
