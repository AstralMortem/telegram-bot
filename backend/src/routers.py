from aiogram import Router
from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    WebAppInfo,
    InlineKeyboardMarkup,
)
from aiogram.filters import CommandStart
from config import settings

router = Router()


@router.message(CommandStart())
async def start_command(msg: Message):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Open app", web_app=WebAppInfo(url=settings.FRONT_URL)
                )
            ]
        ]
    )
    await msg.reply("Hello", reply_markup=markup)
