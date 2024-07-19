from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message

from db.schemas import UserAddDTO

from services import UserService


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
            UserAddDTO(id=event.from_user.id, username=event.from_user.username)
        )
        data["user"] = user
        return await handler(event, data)
