from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔎 Vakansiyalar"),
            KeyboardButton(text="📍 Shahar"),
        ],
        [
            KeyboardButton(text="💼 Kasb"),
            KeyboardButton(text="💰 Maosh"),
        ],
        [
            KeyboardButton(text="⭐ Saqlanganlar"),
            KeyboardButton(text="📋 Arizalarim"),
        ],
        [
            KeyboardButton(text="👤 Profil"),
        ],
    ],
    resize_keyboard=True,
)