from contextlib import asynccontextmanager
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from aiogram.types import Update
from utils import UserMiddleware
from config import settings, WEBHOOK_URL
from routers.handlers import router as bot_router
from routers.webhooks import router as webhook_router
from routers.api import api_router
from db.connect import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_info = await bot.get_webhook_info()
    if(webhook_info.url != WEBHOOK_URL):
        await bot.set_webhook(url=WEBHOOK_URL, allowed_updates=dp.resolve_used_update_types(),drop_pending_updates=True,)
    await init_db()
    yield

    await bot.session.close()
    logging.info("Bot stopped")

bot = Bot(token=settings.BOT_TOKEN,default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(','),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
app.include_router(webhook_router)

@app.post(settings.WEBHOOK_PATH)
async def webhook(request: Request):
    telegram_update = Update.model_validate(await request.json(), context={"bot":bot})
    await dp.feed_update(bot, telegram_update)


dp.include_router(bot_router)
dp.message.middleware(UserMiddleware())





