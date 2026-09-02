from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message(lambda message: message.text == "📋 Arizalarim")
async def applications_handler(message: Message):
    await message.answer(
        "📋 Arizalarim\n\n"
        "Siz hali hech qanday ariza yubormagansiz."
    )