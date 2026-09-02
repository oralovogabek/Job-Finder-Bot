from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.states.job_search import JobSearchState
from app.keyboards.jobs import (
    job_search_keyboard,
    cities_keyboard,
    salary_keyboard,
)


router = Router()


# =========================
# 📍 SHAHAR
# =========================

@router.message(F.text == "📍 Shahar")
async def choose_city(message: Message, state: FSMContext):

    await state.set_state(JobSearchState.city)

    await message.answer(
        "📍 Ish qidirayotgan shaharingizni tanlang:",
        reply_markup=cities_keyboard()
    )


@router.message(JobSearchState.city)
async def selected_city(message: Message, state: FSMContext):

    if message.text == "⬅️ Orqaga":
        await state.clear()

        await message.answer(
            "Asosiy qidiruv menyusi:",
            reply_markup=job_search_keyboard()
        )
        return

    cities = [
        "Toshkent",
        "Samarqand",
        "Buxoro",
        "Andijon",
        "Namangan",
        "Farg‘ona",
        "Xorazm",
        "Qashqadaryo",
    ]

    if message.text not in cities:
        await message.answer(
            "❌ Iltimos, ro‘yxatdan shahar tanlang.",
            reply_markup=cities_keyboard()
        )
        return

    await state.update_data(city=message.text)

    await state.clear()

    await message.answer(
        f"✅ Shahar tanlandi: {message.text}\n\n"
        "Endi kerakli maoshni tanlang.",
        reply_markup=job_search_keyboard()
    )


# =========================
# 💰 MAOSH
# =========================

@router.message(F.text == "💰 Maosh")
async def choose_salary(message: Message, state: FSMContext):

    await state.set_state(JobSearchState.salary)

    await message.answer(
        "💰 Minimal maoshni tanlang:",
        reply_markup=salary_keyboard()
    )


@router.message(JobSearchState.salary)
async def selected_salary(message: Message, state: FSMContext):

    if message.text == "⬅️ Orqaga":
        await state.clear()

        await message.answer(
            "Asosiy qidiruv menyusi:",
            reply_markup=job_search_keyboard()
        )
        return

    salaries = {
        "3 000 000": 3000000,
        "5 000 000": 5000000,
        "7 000 000": 7000000,
        "10 000 000": 10000000,
        "15 000 000": 15000000,
        "20 000 000": 20000000,
    }

    if message.text not in salaries:
        await message.answer(
            "❌ Iltimos, ro‘yxatdan maosh tanlang.",
            reply_markup=salary_keyboard()
        )
        return

    salary = salaries[message.text]

    await state.update_data(salary=salary)

    await state.clear()

    await message.answer(
        f"✅ Minimal maosh: {message.text} so‘m",
        reply_markup=job_search_keyboard()
    )


# =========================
# 💼 KASB
# =========================

@router.message(F.text == "💼 Kasb")
async def choose_profession(message: Message, state: FSMContext):

    await state.set_state(JobSearchState.profession)

    await message.answer(
        "💼 Qaysi kasb bo‘yicha ish qidiryapsiz?\n\n"
        "Masalan:\n"
        "Python Developer\n"
        "Frontend Developer\n"
        "Logist\n"
        "Sotuvchi"
    )


@router.message(JobSearchState.profession)
async def selected_profession(message: Message, state: FSMContext):

    await state.update_data(profession=message.text)

    data = await state.get_data()

    await state.clear()

    city = data.get("city", "Tanlanmagan")
    salary = data.get("salary", "Tanlanmagan")

    await message.answer(
        "✅ Qidiruv ma'lumotlari saqlandi!\n\n"
        f"📍 Shahar: {city}\n"
        f"💰 Maosh: {salary} so‘m\n"
        f"💼 Kasb: {message.text}",
        reply_markup=job_search_keyboard()
    )


# =========================
# 🔎 QIDIRISH
# =========================

@router.message(F.text == "🔎 Qidirish")
async def search_jobs(message: Message, state: FSMContext):

    data = await state.get_data()

    city = data.get("city", "Barcha shaharlar")
    salary = data.get("salary", "Farqi yo‘q")
    profession = data.get("profession", "Barcha kasblar")

    await message.answer(
        "🔎 Ishlar qidirilmoqda...\n\n"
        f"📍 Shahar: {city}\n"
        f"💰 Maosh: {salary}\n"
        f"💼 Kasb: {profession}"
    )


# =========================
# ❌ BEKOR QILISH
# =========================

@router.message(F.text == "❌ Bekor qilish")
async def cancel_search(message: Message, state: FSMContext):

    await state.clear()

    await message.answer(
        "❌ Qidiruv bekor qilindi.",
        reply_markup=job_search_keyboard()
    )  