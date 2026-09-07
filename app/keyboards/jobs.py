from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def search_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📍 Shahar bo‘yicha",
                    callback_data="search_city"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💰 Maosh bo‘yicha",
                    callback_data="search_salary"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔎 Ish/Kasb bo‘yicha",
                    callback_data="search_profession"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Barcha vakansiyalar",
                    callback_data="all_jobs"
                )
            ]
        ]
    )


def job_detail_keyboard(job_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📄 Ariza yuborish",
                    callback_data=f"apply:{job_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❤️ Sevimliga qo‘shish",
                    callback_data=f"favorite:{job_id}"
                )
            ]
        ]
    )