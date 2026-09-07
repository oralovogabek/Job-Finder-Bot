from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_keyboard():

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="➕ Vakansiya qo‘shish"
                ),
                KeyboardButton(
                    text="📋 Vakansiyalar"
                )
            ],
            [
                KeyboardButton(
                    text="📄 Arizalar"
                ),
                KeyboardButton(
                    text="📊 Statistika"
                )
            ],
            [
                KeyboardButton(
                    text="❌ Admin panelni yopish"
                )
            ]
        ],
        resize_keyboard=True
    )


def admin_cancel_keyboard():

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="❌ Bekor qilish"
                )
            ]
        ],
        resize_keyboard=True
    )