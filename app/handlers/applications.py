from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.keyboards.main import main_keyboard

router = Router()

# Hozircha vaqtinchalik xotira.
# Keyingi bosqichda PostgreSQL'ga o'tkazamiz.
user_applications = {}


def add_application(
    user_id: int,
    job: dict,
    full_name: str,
    phone: str,
    message_text: str
):
    if user_id not in user_applications:
        user_applications[user_id] = []

    # Bir vakansiyaga ikki marta ariza yuborishni oldini olish
    for application in user_applications[user_id]:
        if application["job_id"] == job["id"]:
            return False

    application = {
        "job_id": job["id"],
        "title": job["title"],
        "company": job["company"],
        "city": job["city"],
        "salary": job["salary"],
        "profession": job["profession"],

        "user_id": user_id,
        "full_name": full_name,
        "phone": phone,
        "message": message_text,

        "status": "Ko‘rib chiqilmoqda"
    }

    user_applications[user_id].append(application)

    return True


@router.message(F.text == "📄 Arizalarim")
async def applications_handler(
    message: Message,
    state: FSMContext
):
    await state.clear()

    user_id = message.from_user.id
    applications = user_applications.get(user_id, [])

    if not applications:
        await message.answer(
            "📄 <b>Arizalarim</b>\n\n"
            "😔 Siz hali hech qanday vakansiyaga ariza yubormagansiz.\n\n"
            "💼 Vakansiyalar bo‘limiga kirib, o‘zingizga mos ishni toping.",
            reply_markup=main_keyboard(),
            parse_mode="HTML"
        )
        return

    await message.answer(
        f"📄 <b>Arizalarim</b>\n\n"
        f"📊 Jami arizalar: {len(applications)} ta",
        reply_markup=main_keyboard(),
        parse_mode="HTML"
    )

    for application in applications:

        salary = f"{application['salary']:,}".replace(",", " ")

        await message.answer(
            "📩 <b>Ariza</b>\n\n"
            f"💼 <b>{application['title']}</b>\n"
            f"🏢 Kompaniya: {application['company']}\n"
            f"📍 Shahar: {application['city']}\n"
            f"👨‍💻 Kasb: {application['profession']}\n"
            f"💰 Maosh: {salary} so‘m\n\n"
            f"📌 Holati: <b>{application['status']}</b>",
            parse_mode="HTML"
        )