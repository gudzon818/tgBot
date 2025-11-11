from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="/help"),
            KeyboardButton(text="/ping"),
        ],
        [
            KeyboardButton(text="/feedback"),
            KeyboardButton(text="/lang"),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
