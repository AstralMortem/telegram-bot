from fastapi import APIRouter, Request
from aiogram.types import Update


router = APIRouter()


@router.post("/webhook")
async def webhook(request: Request):
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
