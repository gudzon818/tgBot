from aiogram import Router, types, F

router = Router()


@router.callback_query(F.data.startswith("rate:"))
async def rate_callback(call: types.CallbackQuery) -> None:
    value = call.data.split(":", 1)[1]
    text = "Спасибо за оценку! 👍" if value == "like" else "Понял, постараемся лучше 👌"
    await call.answer()
    if call.message:
        await call.message.answer(text)
