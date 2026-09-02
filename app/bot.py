import asyncio

from aiogram import Bot, Dispatcher

from app.config import BOT_TOKEN

from app.handlers.start import router as start_router
from app.handlers.jobs import router as jobs_router
from app.handlers.profile import router as profile_router
from app.handlers.favorites import router as favorites_router
from app.handlers.applications import router as applications_router


async def main():
    bot = Bot(token=BOT_TOKEN)

    dp = Dispatcher()

    # Routers
    dp.include_router(start_router)
    dp.include_router(jobs_router)
    dp.include_router(profile_router)
    dp.include_router(favorites_router)
    dp.include_router(applications_router)

    print("🤖 Job Finder Bot ishga tushdi!")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())