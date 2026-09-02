from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def job_search_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📍 Shahar"),
                KeyboardButton(text="💰 Maosh"),
            ],
            [
                KeyboardButton(text="💼 Kasb"),
                KeyboardButton(text="🔎 Qidirish"),
            ],
            [
                KeyboardButton(text="❌ Bekor qilish"),
            ],
        ],
        resize_keyboard=True
    )


def cities_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Toshkent"),
                KeyboardButton(text="Samarqand"),
            ],
            [
                KeyboardButton(text="Buxoro"),
                KeyboardButton(text="Andijon"),
            ],
            [
                KeyboardButton(text="Namangan"),
                KeyboardButton(text="Farg‘ona"),
            ],
            [
                KeyboardButton(text="Xorazm"),
                KeyboardButton(text="Qashqadaryo"),
            ],
            [
                KeyboardButton(text="⬅️ Orqaga"),
            ],
        ],
        resize_keyboard=True
    )


def salary_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="3 000 000"),
                KeyboardButton(text="5 000 000"),
            ],
            [
                KeyboardButton(text="7 000 000"),
                KeyboardButton(text="10 000 000"),
            ],
            [
                KeyboardButton(text="15 000 000"),
                KeyboardButton(text="20 000 000"),
            ],
            [
                KeyboardButton(text="⬅️ Orqaga"),
            ],
        ],
        resize_keyboard=True
    )