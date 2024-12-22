import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import API_TOKEN
from handlers import register_all_handlers
from tortoise import Tortoise
from config import init_db


async def main():
    await init_db()
    try:
        bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
        dp = Dispatcher()
        register_all_handlers(dp)
        await dp.start_polling(bot)
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(main())