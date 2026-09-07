from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.states.job_search import JobSearchState
from app.states.applications import ApplicationState
from app.keyboards.jobs import search_keyboard, job_detail_keyboard
from app.handlers.applications import add_application


router = Router()


# =========================
# VACANCIES
# =========================

VACANCIES = [
    {
        "id": 1,
        "title": "Python Backend Developer",
        "company": "IT Company",
        "city": "Toshkent",
        "salary": 10000000,
        "profession": "Python Developer"
    },
    {
        "id": 2,
        "title": "Frontend Developer",
        "company": "Digital Agency",
        "city": "Toshkent",
        "salary": 8000000,
        "profession": "Frontend Developer"
    },
    {
        "id": 3,
        "title": "SMM Manager",
        "company": "Marketing Group",
        "city": "Samarqand",
        "salary": 6000000,
        "profession": "SMM Manager"
    },
]


# =========================
# 💼 VAKANSIYALAR
# =========================

@router.message(F.text == "💼 Vakansiyalar")
async def vacancies_handler(
    message: Message,
    state: FSMContext
):

    await state.clear()
    await state.set_state(JobSearchState.choosing)

    await message.answer(
        "💼 <b>Vakansiyalar</b>\n\n"
        "🔎 Ish qidirish usulini tanlang:",
        reply_markup=search_keyboard(),
        parse_mode="HTML"
    )


# =========================
# 📍 SHAHAR BO‘YICHA
# =========================

@router.callback_query(F.data == "search_city")
async def search_city(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.set_state(JobSearchState.city)

    await callback.message.answer(
        "📍 <b>Shaharni kiriting:</b>\n\n"
        "Masalan:\n"
        "Toshkent\n"
        "Samarqand\n"
        "Buxoro\n\n"
        "❌ Bekor qilish"
        ,
        parse_mode="HTML"
    )

    await callback.answer()


@router.message(JobSearchState.city)
async def city_result(
    message: Message,
    state: FSMContext
):

    if message.text == "❌ Bekor qilish":
        await state.clear()

        await message.answer(
            "❌ Qidiruv bekor qilindi."
        )
        return

    city = message.text.strip().lower()

    jobs = [
        job for job in VACANCIES
        if city in job["city"].lower()
    ]

    await state.clear()

    if not jobs:

        await message.answer(
            "😔 Bu shaharda hozircha vakansiya topilmadi."
        )
        return

    await message.answer(
        f"🔎 <b>{message.text.strip()}</b> bo‘yicha "
        f"{len(jobs)} ta vakansiya topildi.",
        parse_mode="HTML"
    )

    for job in jobs:
        await show_job(message, job)


# =========================
# 💰 MAOSH BO‘YICHA
# =========================

@router.callback_query(F.data == "search_salary")
async def search_salary(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.set_state(JobSearchState.salary)

    await callback.message.answer(
        "💰 <b>Minimal maoshni kiriting:</b>\n\n"
        "Masalan:\n"
        "5000000\n\n"
        "Agar 5 000 000 deb kiritsangiz,\n"
        "5 million va undan yuqori maoshli ishlar chiqadi.\n\n"
        "❌ Bekor qilish",
        parse_mode="HTML"
    )

    await callback.answer()


@router.message(JobSearchState.salary)
async def salary_result(
    message: Message,
    state: FSMContext
):

    if message.text == "❌ Bekor qilish":
        await state.clear()

        await message.answer(
            "❌ Qidiruv bekor qilindi."
        )
        return

    try:
        salary = int(
            message.text.replace(" ", "")
        )
    except ValueError:

        await message.answer(
            "❌ Iltimos, faqat raqam kiriting.\n\n"
            "Masalan: 5000000"
        )
        return

    jobs = [
        job for job in VACANCIES
        if job["salary"] >= salary
    ]

    await state.clear()

    if not jobs:

        await message.answer(
            "😔 Bunday maoshga mos vakansiya topilmadi."
        )
        return

    await message.answer(
        f"💰 {salary:,}".replace(",", " ") +
        " so‘m va undan yuqori maoshli ishlar:",
        parse_mode="HTML"
    )

    for job in jobs:
        await show_job(message, job)


# =========================
# 🔎 KASB BO‘YICHA
# =========================

@router.callback_query(F.data == "search_profession")
async def search_profession(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.set_state(
        JobSearchState.profession
    )

    await callback.message.answer(
        "🔎 <b>Ish yoki kasb nomini kiriting:</b>\n\n"
        "Masalan:\n"
        "Python\n"
        "Frontend\n"
        "SMM\n"
        "Backend\n\n"
        "❌ Bekor qilish",
        parse_mode="HTML"
    )

    await callback.answer()


@router.message(JobSearchState.profession)
async def profession_result(
    message: Message,
    state: FSMContext
):

    if message.text == "❌ Bekor qilish":
        await state.clear()

        await message.answer(
            "❌ Qidiruv bekor qilindi."
        )
        return

    profession = message.text.strip().lower()

    jobs = [
        job for job in VACANCIES
        if profession in job["title"].lower()
        or profession in job["profession"].lower()
    ]

    await state.clear()

    if not jobs:

        await message.answer(
            "😔 Siz qidirgan kasb bo‘yicha vakansiya topilmadi."
        )
        return

    await message.answer(
        f"🔎 <b>{message.text.strip()}</b> bo‘yicha "
        f"{len(jobs)} ta vakansiya topildi.",
        parse_mode="HTML"
    )

    for job in jobs:
        await show_job(message, job)


# =========================
# 📋 BARCHA VAKANSIYALAR
# =========================

@router.callback_query(F.data == "all_jobs")
async def all_jobs(callback: CallbackQuery):

    if not VACANCIES:

        await callback.message.answer(
            "😔 Hozircha vakansiyalar mavjud emas."
        )

        await callback.answer()
        return

    await callback.message.answer(
        f"📋 <b>Barcha vakansiyalar</b>\n\n"
        f"Jami: {len(VACANCIES)} ta",
        parse_mode="HTML"
    )

    for job in VACANCIES:
        await show_job(
            callback.message,
            job
        )

    await callback.answer()


# =========================
# 💼 VAKANSIYA KO‘RSATISH
# =========================

async def show_job(
    message: Message,
    job: dict
):

    salary = f"{job['salary']:,}".replace(",", " ")

    await message.answer(
        "💼 <b>Vakansiya</b>\n\n"
        f"💼 <b>{job['title']}</b>\n"
        f"🏢 Kompaniya: {job['company']}\n"
        f"📍 Shahar: {job['city']}\n"
        f"👨‍💻 Kasb: {job['profession']}\n"
        f"💰 Maosh: {salary} so‘m\n\n"
        "👇 Kerakli amalni tanlang:",
        reply_markup=job_detail_keyboard(
            job["id"]
        ),
        parse_mode="HTML"
    )


# =========================
# 📄 ARIZA BOSHLASH
# =========================

@router.callback_query(F.data.startswith("apply:"))
async def apply_start(
    callback: CallbackQuery,
    state: FSMContext
):

    job_id = int(
        callback.data.split(":")[1]
    )

    job = next(
        (
            job for job in VACANCIES
            if job["id"] == job_id
        ),
        None
    )

    if not job:

        await callback.answer(
            "❌ Vakansiya topilmadi.",
            show_alert=True
        )
        return

    await state.clear()

    await state.update_data(
        job_id=job_id
    )

    await state.set_state(
        ApplicationState.full_name
    )

    await callback.message.answer(
        "📄 <b>Ariza yuborish</b>\n\n"
        "1️⃣ Ism va familiyangizni kiriting.\n\n"
        "Masalan:\n"
        "Ali Valiyev\n\n"
        "❌ Bekor qilish",
        parse_mode="HTML"
    )

    await callback.answer()


# =========================
# 👤 ISM FAMILIYA
# =========================

@router.message(ApplicationState.full_name)
async def application_full_name(
    message: Message,
    state: FSMContext
):

    if message.text == "❌ Bekor qilish":

        await state.clear()

        await message.answer(
            "❌ Ariza yuborish bekor qilindi."
        )
        return

    if not message.text or len(
        message.text.strip()
    ) < 2:

        await message.answer(
            "❌ Iltimos, ism va familiyangizni kiriting."
        )
        return

    await state.update_data(
        full_name=message.text.strip()
    )

    await state.set_state(
        ApplicationState.phone
    )

    await message.answer(
        "2️⃣ 📱 Telefon raqamingizni kiriting.\n\n"
        "Masalan:\n"
        "+998901234567"
    )


# =========================
# 📱 TELEFON
# =========================

@router.message(ApplicationState.phone)
async def application_phone(
    message: Message,
    state: FSMContext
):

    if message.text == "❌ Bekor qilish":

        await state.clear()

        await message.answer(
            "❌ Ariza yuborish bekor qilindi."
        )
        return

    phone = message.text.strip()

    if not phone.startswith("+998"):

        await message.answer(
            "❌ Telefon raqami noto‘g‘ri.\n\n"
            "Masalan:\n"
            "+998901234567"
        )
        return

    await state.update_data(
        phone=phone
    )

    await state.set_state(
        ApplicationState.message
    )

    await message.answer(
        "3️⃣ 📝 O‘zingiz haqingizda qisqacha yozing.\n\n"
        "Masalan:\n"
        "Python va PostgreSQL bilan ishlayman.\n"
        "Backend dasturlash bo‘yicha tajribam bor."
    )


# =========================
# 📝 O‘ZI HAQIDA
# =========================

@router.message(ApplicationState.message)
async def application_message(
    message: Message,
    state: FSMContext
):

    if message.text == "❌ Bekor qilish":

        await state.clear()

        await message.answer(
            "❌ Ariza yuborish bekor qilindi."
        )
        return

    if not message.text or len(
        message.text.strip()
    ) < 5:

        await message.answer(
            "❌ Iltimos, o‘zingiz haqingizda "
            "biroz batafsilroq yozing."
        )
        return

    await state.update_data(
        message_text=message.text.strip()
    )

    data = await state.get_data()

    job = next(
        (
            job for job in VACANCIES
            if job["id"] == data["job_id"]
        ),
        None
    )

    if not job:

        await state.clear()

        await message.answer(
            "❌ Vakansiya topilmadi."
        )
        return

    success = add_application(
        user_id=message.from_user.id,
        job=job,
        full_name=data["full_name"],
        phone=data["phone"],
        message_text=data["message_text"]
    )

    await state.clear()

    if not success:

        await message.answer(
            "⚠️ Siz bu vakansiyaga oldin "
            "ariza yuborgansiz."
        )
        return

    await message.answer(
        "✅ <b>Arizangiz muvaffaqiyatli yuborildi!</b>\n\n"
        f"💼 {job['title']}\n"
        f"🏢 {job['company']}\n"
        f"📍 {job['city']}\n\n"
        "📌 Holati: <b>Ko‘rib chiqilmoqda</b>\n\n"
        "👨‍💼 Admin arizangizni ko‘rib chiqadi.",
        parse_mode="HTML"
    )