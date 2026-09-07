import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import BOT_TOKEN

from app.handlers import start
from app.handlers import jobs
from app.handlers import profile
from app.handlers import applications
from app.handlers import admin


async def main():

    bot = Bot(
        token=BOT_TOKEN
    )

    dp = Dispatcher(
        storage=MemoryStorage()
    )

    dp.include_router(
        start.router
    )

    dp.include_router(
        jobs.router
    )

    dp.include_router(
        profile.router
    )

    dp.include_router(
        applications.router
    )

    dp.include_router(
        admin.router
    )

    await bot.delete_webhook(
        drop_pending_updates=True
    )

    print(
        "🤖 Job Finder Bot ishga tushdi!"
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())