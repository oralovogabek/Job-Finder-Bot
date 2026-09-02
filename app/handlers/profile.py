from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message(lambda message: message.text == "👤 Profil")
async def profile_handler(message: Message):
    await message.answer(
        "👤 Profil\n\n"
        f"Ism: {message.from_user.full_name}\n"
        f"Username: @{message.from_user.username or 'yo‘q'}\n"
        f"Telegram ID: {message.from_user.id}"
    )