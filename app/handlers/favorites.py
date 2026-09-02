from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message(lambda message: message.text == "⭐ Saqlanganlar")
async def favorites_handler(message: Message):
    await message.answer(
        "⭐ Saqlanganlar\n\n"
        "Hozircha saqlangan vakansiyalar yo‘q."
    )