from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def items_kb(page: int, has_prev: bool, has_next: bool) -> InlineKeyboardMarkup:
    buttons = []
    nav = []
    if has_prev:
        nav.append(InlineKeyboardButton(text="⬅️ Prev", callback_data=f"items:page:{page-1}"))
    nav.append(InlineKeyboardButton(text=f"Page {page}", callback_data="items:noop"))
    if has_next:
        nav.append(InlineKeyboardButton(text="Next ➡️", callback_data=f"items:page:{page+1}"))
    buttons.append(nav)
    return InlineKeyboardMarkup(inline_keyboard=buttons)
