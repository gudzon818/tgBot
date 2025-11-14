from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.i18n.translator import t


def main_menu(lang: str = "ru", is_admin: bool = False) -> ReplyKeyboardMarkup:
    # 1 ряд: игровые действия
    row1 = [
        KeyboardButton(text=t("menu_daily", lang)),
        KeyboardButton(text=t("menu_d20", lang)),
        KeyboardButton(text=t("menu_quiz", lang)),
    ]
    # 2 ряд: цитата, гороскоп, настроение, помощь и (для админа) админ‑меню
    row2: list[KeyboardButton] = [
        KeyboardButton(text=t("menu_quote", lang)),
        KeyboardButton(text=t("menu_horoscope", lang)),
        KeyboardButton(text=t("menu_mood", lang)),
        KeyboardButton(text=t("menu_help", lang)),
    ]
    if is_admin:
        row2.append(KeyboardButton(text=t("menu_admin_help", lang)))
    kb = [row1, row2]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
