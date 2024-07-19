import asyncio
from contextlib import asynccontextmanager
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fastapi import FastAPI
from config import settings
from handlers import router
from routers import api_router
from db.connect import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


async def main():
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    app = FastAPI(lifespan=lifespan)

    app.include_router(api_router)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
