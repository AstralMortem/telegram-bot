from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, UserProfilePhotos
import socketio
from .config import settings
from .db.schemas import UserAddDTO
from .services import UserService

sio = socketio.AsyncServer(
    async_mode="asgi", logger=True, cors_allowed_origins=[], transports=["websocket"]
)


async def get_user_photo(user_id: int, bot: Bot):
    result: UserProfilePhotos = await bot.get_user_profile_photos(user_id, limit=1)
    if len(result.photos) > 0:
        files = await bot.get_file(result.photos[0][0].file_id)
        url = f"https://api.telegram.org/file/bot{settings.BOT_TOKEN}/{files.file_path}"
        return url
    return None


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        service = UserService()
        if not event.from_user or not event.from_user.username:
            return await event.answer("You need to set your username to use this bot.")

        if event.from_user.is_bot:
            return await event.answer("Bots can`t use this app")

        user = await service.create_user(
            UserAddDTO(
                id=event.from_user.id,
                username=event.from_user.username,
                image_url=await get_user_photo(event.from_user.id, event.bot),
            )
        )

        data["user"] = user
        return await handler(event, data)
