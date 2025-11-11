from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.i18n.translator import t


def like_dislike_kb(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("like", lang), callback_data="rate:like"),
                InlineKeyboardButton(text=t("dislike", lang), callback_data="rate:dislike"),
            ]
        ]
    )
