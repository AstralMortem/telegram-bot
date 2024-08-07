from typing import Annotated
from fastapi import APIRouter, Depends
from ..db.schemas import GoldBody, Pagination
from ..services import UserService, GoldService
from ..utils import sio

api_router = APIRouter(prefix="/api")

user_service = Annotated[UserService, Depends(UserService)]
gold_service = Annotated[GoldService, Depends(GoldService)]


@api_router.get("/users")
async def get_users(service: user_service, pagination: Pagination = Depends()):
    return await service.get_users(pagination)


@api_router.get("/users/{user_id}")
async def get_user_profile(user_id: int, service: user_service):
    return await service.get_user(user_id)


# @api_router.post("/users")
# async def create_user(service: user_service, data: UserAddDTO):
#     return await service.create_user(data)


@api_router.post("/buy_gold")
async def buy_gold(service: gold_service, data: GoldBody):
    gold, user = await service.buy_gold(data.user_id, data.amount)
    await sio.emit("gold:get", gold.model_dump_json())
    await sio.emit("user:current", user.model_dump_json())
    return user


@api_router.post("/sell_gold")
async def sell_gold(service: gold_service, data: GoldBody):
    gold, user = await service.sell_gold(data.user_id, data.amount)
    await sio.emit("gold:get", gold.model_dump_json())
    await sio.emit("user:current", gold.model_dump_json())
    return user


@api_router.get("/gold")
async def get_gold(service: gold_service):
    return await service.get_last_gold()
