import asyncio

from sqlalchemy import text

from app.database.database import engine


async def test_database():
    async with engine.connect() as connection:
        result = await connection.execute(text("SELECT 1"))
        print("Database javobi:", result.scalar())


if __name__ == "__main__":
    asyncio.run(test_database())