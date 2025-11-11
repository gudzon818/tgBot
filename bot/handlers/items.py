from aiogram import Router, types, F
from aiogram.filters import Command
from bot.keyboards.items import items_kb

router = Router()


def get_page_items(page: int, per_page: int = 5) -> tuple[list[str], bool, bool]:
    # Demo data: 42 items
    total = 42
    start = (page - 1) * per_page
    end = start + per_page
    items = [f"Item #{i+1}" for i in range(start, min(end, total))]
    has_prev = page > 1
    has_next = end < total
    return items, has_prev, has_next


@router.message(Command("items"))
async def cmd_items(message: types.Message) -> None:
    page = 1
    items, has_prev, has_next = get_page_items(page)
    text = "\n".join(items) or "Нет элементов"
    await message.answer(text, reply_markup=items_kb(page, has_prev, has_next))


@router.callback_query(F.data.startswith("items:page:"))
async def paginate(call: types.CallbackQuery) -> None:
    try:
        page = int(call.data.split(":")[-1])
        page = max(1, page)
    except Exception:
        page = 1
    items, has_prev, has_next = get_page_items(page)
    text = "\n".join(items) or "Нет элементов"
    if call.message:
        await call.message.edit_text(text, reply_markup=items_kb(page, has_prev, has_next))
    await call.answer()
