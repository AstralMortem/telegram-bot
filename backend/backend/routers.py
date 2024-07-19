from typing import Annotated
from fastapi import APIRouter, Depends
from schemas import Pagination, UserAddDTO
from services import UserService, GoldService

api_router = APIRouter()

user_service = Annotated[UserService, Depends(UserService)]
gold_service = Annotated[GoldService, Depends(GoldService)]


@api_router.get("/users")
async def get_users(service: user_service, pagination: Pagination = Depends()):
    return await service.get_users(pagination)


@api_router.get("/users/{user_id}")
async def get_user_profile(user_id: str, service: user_service):
    return await service.get_user_by_tg(user_id)


@api_router.post("/users")
async def create_user(service: user_service, data: UserAddDTO):
    return await service.create_user(data)


@api_router.post("/buy_gold")
async def buy_gold(service: gold_service, user_id: str, amount: float):
    return await service.buy_gold(user_id, amount)


@api_router.post("/sell_gold")
async def sell_gold(service: gold_service, user_id: str, amount: float):
    return await service.sell_gold(user_id, amount)


@api_router.get("/gold")
async def get_gold(service: gold_service):
    return await service.get_last_gold()
