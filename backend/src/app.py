import asyncio
from aiogram import Bot, Dispatcher
from routers import router as main_router
from config import settings


async def main():
    bot = Bot(settings.BOT_TOKEN)

    dp = Dispatcher()
    dp.include_router(main_router)

    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
