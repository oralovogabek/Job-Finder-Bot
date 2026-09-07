from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.keyboards.main import main_keyboard
from app.states.job_search import JobSearchState


router = Router()


@router.message(CommandStart())
async def start_handler(
    message: Message,
    state: FSMContext
):
    await state.clear()

    await state.set_state(
        JobSearchState.choosing
    )

    await message.answer(
        f"👋 Assalomu alaykum, "
        f"{message.from_user.first_name}!\n\n"
        "🤖 Job Finder Botga xush kelibsiz!\n\n"
        "🔎 Keling, sizga mos ishni topamiz.",
        reply_markup=main_keyboard()
    )