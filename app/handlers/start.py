from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.keyboards.main import main_keyboard


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "👋 Assalomu alaykum!\n\n"
        "💼 Job Finder Bot'ga xush kelibsiz!\n\n"
        "Bu bot orqali siz:\n"
        "🔎 Vakansiyalarni qidirishingiz\n"
        "⭐ Vakansiyalarni saqlashingiz\n"
        "📋 Arizalaringizni ko‘rishingiz\n"
        "👤 Profilingizni boshqarishingiz mumkin.\n\n"
        "Quyidagi menyudan foydalaning 👇",
        reply_markup=main_keyboard,
    )