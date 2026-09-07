from aiogram import Router, F
from aiogram.types import Message

from app.keyboards.main import main_keyboard

router = Router()


@router.message(F.text == "👤 Profil")
async def profile_handler(message: Message):

    await message.answer(
        "👤 <b>Sizning profilingiz</b>\n\n"
        f"🆔 Telegram ID: <code>{message.from_user.id}</code>\n"
        f"👤 Ism: {message.from_user.first_name or 'Kiritilmagan'}\n"
        f"📝 Username: @{message.from_user.username or 'Mavjud emas'}\n\n"
        "🏠 Asosiy menyudan kerakli bo‘limni tanlang.",
        reply_markup=main_keyboard(),
        parse_mode="HTML"
    )