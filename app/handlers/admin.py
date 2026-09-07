from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext

from app.config import ADMIN_IDS

from app.keyboards.admin import (
    admin_keyboard,
    admin_cancel_keyboard
)

from app.keyboards.main import main_keyboard

from app.states.admin import AdminJobState

from app.handlers.jobs import VACANCIES

from app.handlers.applications import user_applications


router = Router()


# =========================
# ADMIN TEKSHIRISH
# =========================

def is_admin(user_id: int) -> bool:

    return user_id in ADMIN_IDS


# =========================
# ARIZA TUGMALARI
# =========================

def application_keyboard(
    user_id: int,
    job_id: int
):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Qabul qilish",
                    callback_data=f"accept:{user_id}:{job_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Rad etish",
                    callback_data=f"reject:{user_id}:{job_id}"
                )
            ]
        ]
    )


# =========================
# /ADMIN
# =========================

@router.message(Command("admin"))
async def admin_command(
    message: Message,
    state: FSMContext
):

    if not is_admin(message.from_user.id):

        await message.answer(
            "❌ Sizda admin huquqi yo‘q."
        )

        return

    await state.clear()

    await message.answer(
        "👨‍💼 <b>ADMIN PANEL</b>\n\n"
        "Kerakli bo‘limni tanlang:",
        reply_markup=admin_keyboard(),
        parse_mode="HTML"
    )


# =========================
# VAKANSIYA QO'SHISH
# =========================

@router.message(F.text == "➕ Vakansiya qo‘shish")
async def add_job_start(
    message: Message,
    state: FSMContext
):

    if not is_admin(message.from_user.id):
        return

    await state.clear()

    await state.set_state(
        AdminJobState.title
    )

    await message.answer(
        "➕ <b>Yangi vakansiya</b>\n\n"
        "1️⃣ Vakansiya nomini kiriting.\n\n"
        "Masalan:\n"
        "Python Backend Developer",
        reply_markup=admin_cancel_keyboard(),
        parse_mode="HTML"
    )


# =========================
# TITLE
# =========================

@router.message(AdminJobState.title)
async def add_job_title(
    message: Message,
    state: FSMContext
):

    if message.text == "❌ Bekor qilish":

        await state.clear()

        await message.answer(
            "❌ Vakansiya qo‘shish bekor qilindi.",
            reply_markup=admin_keyboard()
        )

        return

    await state.update_data(
        title=message.text.strip()
    )

    await state.set_state(
        AdminJobState.company
    )

    await message.answer(
        "2️⃣ 🏢 Kompaniya nomini kiriting."
    )


# =========================
# COMPANY
# =========================

@router.message(AdminJobState.company)
async def add_job_company(
    message: Message,
    state: FSMContext
):

    if message.text == "❌ Bekor qilish":

        await state.clear()

        await message.answer(
            "❌ Bekor qilindi.",
            reply_markup=admin_keyboard()
        )

        return

    await state.update_data(
        company=message.text.strip()
    )

    await state.set_state(
        AdminJobState.city
    )

    await message.answer(
        "3️⃣ 📍 Shaharni kiriting.\n\n"
        "Masalan:\n"
        "Toshkent"
    )


# =========================
# CITY
# =========================

@router.message(AdminJobState.city)
async def add_job_city(
    message: Message,
    state: FSMContext
):

    if message.text == "❌ Bekor qilish":

        await state.clear()

        await message.answer(
            "❌ Bekor qilindi.",
            reply_markup=admin_keyboard()
        )

        return

    await state.update_data(
        city=message.text.strip()
    )

    await state.set_state(
        AdminJobState.salary
    )

    await message.answer(
        "4️⃣ 💰 Maoshni kiriting.\n\n"
        "Faqat raqam.\n\n"
        "Masalan:\n"
        "10000000"
    )


# =========================
# SALARY
# =========================

@router.message(AdminJobState.salary)
async def add_job_salary(
    message: Message,
    state: FSMContext
):

    if message.text == "❌ Bekor qilish":

        await state.clear()

        await message.answer(
            "❌ Bekor qilindi.",
            reply_markup=admin_keyboard()
        )

        return

    if not message.text.isdigit():

        await message.answer(
            "❌ Maosh faqat raqam bo‘lishi kerak.\n\n"
            "Masalan: 10000000"
        )

        return

    await state.update_data(
        salary=int(message.text)
    )

    await state.set_state(
        AdminJobState.profession
    )

    await message.answer(
        "5️⃣ 👨‍💻 Kasbni kiriting.\n\n"
        "Masalan:\n"
        "Python Developer"
    )


# =========================
# PROFESSION
# =========================

@router.message(AdminJobState.profession)
async def add_job_profession(
    message: Message,
    state: FSMContext
):

    if message.text == "❌ Bekor qilish":

        await state.clear()

        await message.answer(
            "❌ Bekor qilindi.",
            reply_markup=admin_keyboard()
        )

        return

    await state.update_data(
        profession=message.text.strip()
    )

    data = await state.get_data()

    new_id = max(
        [job["id"] for job in VACANCIES],
        default=0
    ) + 1

    new_job = {
        "id": new_id,
        "title": data["title"],
        "company": data["company"],
        "city": data["city"],
        "salary": data["salary"],
        "profession": data["profession"]
    }

    VACANCIES.append(new_job)

    await state.clear()

    salary = f"{data['salary']:,}".replace(",", " ")

    await message.answer(
        "✅ <b>Vakansiya qo‘shildi!</b>\n\n"
        f"🆔 ID: {new_id}\n"
        f"💼 {data['title']}\n"
        f"🏢 {data['company']}\n"
        f"📍 {data['city']}\n"
        f"💰 {salary} so‘m\n"
        f"👨‍💻 {data['profession']}",
        reply_markup=admin_keyboard(),
        parse_mode="HTML"
    )


# =========================
# ADMIN VAKANSIYALARI
# =========================

@router.message(F.text == "📋 Vakansiyalar")
async def admin_jobs(
    message: Message
):

    if not is_admin(message.from_user.id):
        return

    if not VACANCIES:

        await message.answer(
            "📋 Hozircha vakansiyalar yo‘q.",
            reply_markup=admin_keyboard()
        )

        return

    await message.answer(
        f"📋 <b>Vakansiyalar</b>\n\n"
        f"Jami: {len(VACANCIES)} ta",
        parse_mode="HTML"
    )

    for job in VACANCIES:

        salary = f"{job['salary']:,}".replace(",", " ")

        await message.answer(
            f"🆔 ID: {job['id']}\n\n"
            f"💼 <b>{job['title']}</b>\n"
            f"🏢 {job['company']}\n"
            f"📍 {job['city']}\n"
            f"👨‍💻 {job['profession']}\n"
            f"💰 {salary} so‘m",
            parse_mode="HTML"
        )


# =========================
# ADMIN ARIZALAR
# =========================

@router.message(F.text == "📄 Arizalar")
async def admin_applications(
    message: Message
):

    if not is_admin(message.from_user.id):
        return

    if not user_applications:

        await message.answer(
            "📄 Hozircha hech qanday ariza yo‘q.",
            reply_markup=admin_keyboard()
        )

        return

    total = sum(
        len(applications)
        for applications in user_applications.values()
    )

    await message.answer(
        f"📄 <b>ARIZALAR</b>\n\n"
        f"📊 Jami arizalar: {total} ta",
        parse_mode="HTML"
    )

    for user_id, applications in user_applications.items():

        for application in applications:

            salary = f"{application['salary']:,}".replace(
                ",",
                " "
            )

            await message.answer(
                "📩 <b>YANGI ARIZA</b>\n\n"
                f"👤 Ism: {application['full_name']}\n"
                f"🆔 User ID: {user_id}\n"
                f"📱 Telefon: {application['phone']}\n\n"
                f"💼 Vakansiya: {application['title']}\n"
                f"🏢 Kompaniya: {application['company']}\n"
                f"📍 Shahar: {application['city']}\n"
                f"👨‍💻 Kasb: {application['profession']}\n"
                f"💰 Maosh: {salary} so‘m\n\n"
                f"📝 Nomzod haqida:\n"
                f"{application['message']}\n\n"
                f"📌 Holati: <b>{application['status']}</b>",
                reply_markup=application_keyboard(
                    user_id,
                    application["job_id"]
                ),
                parse_mode="HTML"
            )


# =========================
# QABUL QILISH
# =========================

@router.callback_query(
    F.data.startswith("accept:")
)
async def accept_application(
    callback: CallbackQuery
):

    if not is_admin(callback.from_user.id):

        await callback.answer(
            "❌ Admin huquqi kerak.",
            show_alert=True
        )

        return

    parts = callback.data.split(":")

    user_id = int(parts[1])
    job_id = int(parts[2])

    applications = user_applications.get(
        user_id,
        []
    )

    for application in applications:

        if application["job_id"] != job_id:
            continue

        application["status"] = "Qabul qilindi"

        await callback.message.edit_reply_markup(
            reply_markup=None
        )

        await callback.message.answer(
            "✅ <b>Ariza qabul qilindi!</b>",
            parse_mode="HTML"
        )

        # Foydalanuvchiga xabar
        try:

            await callback.bot.send_message(
                user_id,

                "🎉 <b>Tabriklaymiz!</b>\n\n"
                "Sizning arizangiz qabul qilindi.\n\n"
                f"💼 {application['title']}\n"
                f"🏢 {application['company']}\n"
                f"📍 {application['city']}\n\n"
                "📌 Holati: <b>Qabul qilindi</b>",
                parse_mode="HTML"
            )

        except Exception:

            await callback.message.answer(
                "⚠️ Foydalanuvchiga xabar yuborib bo‘lmadi."
            )

        await callback.answer(
            "✅ Ariza qabul qilindi."
        )

        return

    await callback.answer(
        "❌ Ariza topilmadi.",
        show_alert=True
    )


# =========================
# RAD ETISH
# =========================

@router.callback_query(
    F.data.startswith("reject:")
)
async def reject_application(
    callback: CallbackQuery
):

    if not is_admin(callback.from_user.id):

        await callback.answer(
            "❌ Admin huquqi kerak.",
            show_alert=True
        )

        return

    parts = callback.data.split(":")

    user_id = int(parts[1])
    job_id = int(parts[2])

    applications = user_applications.get(
        user_id,
        []
    )

    for application in applications:

        if application["job_id"] != job_id:
            continue

        application["status"] = "Rad etildi"

        await callback.message.edit_reply_markup(
            reply_markup=None
        )

        await callback.message.answer(
            "❌ <b>Ariza rad etildi.</b>",
            parse_mode="HTML"
        )

        try:

            await callback.bot.send_message(
                user_id,

                "📩 <b>Arizangiz bo‘yicha javob</b>\n\n"
                f"💼 {application['title']}\n"
                f"🏢 {application['company']}\n"
                f"📍 {application['city']}\n\n"
                "📌 Holati: <b>Rad etildi</b>",
                parse_mode="HTML"
            )

        except Exception:

            await callback.message.answer(
                "⚠️ Foydalanuvchiga xabar yuborib bo‘lmadi."
            )

        await callback.answer(
            "❌ Ariza rad etildi."
        )

        return

    await callback.answer(
        "❌ Ariza topilmadi.",
        show_alert=True
    )


# =========================
# STATISTIKA
# =========================

@router.message(F.text == "📊 Statistika")
async def admin_statistics(
    message: Message
):

    if not is_admin(message.from_user.id):
        return

    total_jobs = len(VACANCIES)

    total_applications = sum(
        len(applications)
        for applications in user_applications.values()
    )

    pending = 0
    accepted = 0
    rejected = 0

    for applications in user_applications.values():

        for application in applications:

            if application["status"] == "Ko‘rib chiqilmoqda":
                pending += 1

            elif application["status"] == "Qabul qilindi":
                accepted += 1

            elif application["status"] == "Rad etildi":
                rejected += 1

    await message.answer(
        "📊 <b>STATISTIKA</b>\n\n"
        f"💼 Vakansiyalar: {total_jobs} ta\n"
        f"📄 Jami arizalar: {total_applications} ta\n\n"
        f"🟡 Ko‘rib chiqilmoqda: {pending} ta\n"
        f"🟢 Qabul qilindi: {accepted} ta\n"
        f"🔴 Rad etildi: {rejected} ta",
        reply_markup=admin_keyboard(),
        parse_mode="HTML"
    )


# =========================
# ADMIN PANELNI YOPISH
# =========================

@router.message(F.text == "❌ Admin panelni yopish")
async def close_admin(
    message: Message,
    state: FSMContext
):

    if not is_admin(message.from_user.id):
        return

    await state.clear()

    await message.answer(
        "✅ Admin panel yopildi.",
        reply_markup=main_keyboard()
    )