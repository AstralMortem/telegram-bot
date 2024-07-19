from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)
from db.schemas import UserAddDTO
from services import UserService
from config import settings

router = Router()


@router.message(CommandStart())
async def send_welcome(msg: Message):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Open App",
                    web_app=WebAppInfo(url=settings.WEBAPP_URL),
                )
            ]
        ]
    )
    await msg.reply(text="Open App", reply_markup=markup)
