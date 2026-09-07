from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💼 Vakansiyalar"),
                KeyboardButton(text="👤 Profil"),
            ],
            [
                KeyboardButton(text="❤️ Sevimlilar"),
                KeyboardButton(text="📄 Arizalarim"),
            ],
        ],
        resize_keyboard=True
    )