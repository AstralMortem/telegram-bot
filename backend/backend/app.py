from contextlib import asynccontextmanager
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils import UserMiddleware
from config import settings
from routers.handlers import router as bot_router
from routers.webhooks import router as webhook_router
from routers.api import api_router
from db.connect import init_db
import asyncio

import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # await bot.set_webhook(
    #     url=f"{settings.BACKEND_URL}/webhook",
    #     allowed_updates=dp.resolve_used_update_types(),
    #     drop_pending_updates=True,
    # )
    await init_db()

    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
app.include_router(webhook_router)


async def main():
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(bot_router)
    dp.message.middleware(UserMiddleware())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())