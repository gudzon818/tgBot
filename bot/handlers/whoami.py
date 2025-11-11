from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("whoami"))
async def cmd_whoami(message: types.Message) -> None:
    user = message.from_user
    await message.answer(
        f"Ваш numeric id: <code>{user.id}</code>\n"
        f"Username: @{user.username}" if user.username else f"Username: (нет)"
    )
