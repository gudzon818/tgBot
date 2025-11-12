from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.i18n.translator import t


def main_menu(lang: str = "ru") -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text=t("menu_daily", lang)),
            KeyboardButton(text=t("menu_d20", lang)),
        ],
        [
            KeyboardButton(text=t("menu_quiz", lang)),
            KeyboardButton(text=t("menu_quote", lang)),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
