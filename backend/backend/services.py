import math
from typing import Any
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.testing.util import round_decimal
from .db.connect import sessionmanager
from .db.models import GoldTransaction, User
from .db.schemas import GoldListDTO, Pagination, UserAddDTO, UserListDTO
from .config import settings


class UserService:

    async def get_users(self, pagination: Pagination):
        async with sessionmanager.session() as session:
            stmt = (
                select(User)
                .where(User.is_active == True)
                .limit(pagination.limit)
                .offset(pagination.offset)
            )  # noqa: E712
            instance = await session.scalars(stmt)
            return [UserListDTO.model_validate(user) for user in instance.all()]

    async def get_user(self, id: int):
        async with sessionmanager.session() as session:
            instance = await session.get(User, id)
            if not instance:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "User does not exists")
            return UserListDTO.model_validate(instance)

    async def create_user(self, data: UserAddDTO):
        async with sessionmanager.session() as session:
            try:
                instance = await self.get_user(data.id)
                return instance
            except HTTPException:
                instance = User(**data.model_dump())
                session.add(instance)
                await session.commit()
                return UserListDTO.model_validate(instance)


def calculate_price(token_supply):
    res = (token_supply / settings.INITIAL_GOLD_SUPPLY) ** (
        1 / settings.BOUNDING_CURVE_KOEF - 1
    ) * settings.INITIAL_GOLD_PRICE
    return round_decimal(res, 8)


def calculate_new_supply(tokens_to_transact):
    res = settings.INITIAL_GOLD_SUPPLY * (
        (1 + (tokens_to_transact / settings.INITIAL_GOLD_SUPPLY))
        ** settings.BOUNDING_CURVE_KOEF
        - 1
    )
    return round_decimal(res, 8)


class GoldService:
    async def get_last_gold(self):
        async with sessionmanager.session() as session:
            statement = (
                select(GoldTransaction)
                .order_by(GoldTransaction.created_at.desc())
                .limit(1)
            )
            instance = await session.scalar(statement)
            if not instance:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, "Transaction does not exists"
                )
            result = GoldListDTO.model_validate(instance)
            return result

    async def buy_gold(self, user_id, amount: float):
        async with sessionmanager.session() as session:
            user = await session.get(User, user_id)
            if not user:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "User does not exist")

            gold = await session.scalar(
                select(GoldTransaction)
                .order_by(GoldTransaction.created_at.desc())
                .limit(1)
            )

            if not gold:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, "Transaction does not exist"
                )

            if user.silver_amount < amount:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "Insufficient silver.")

            total_cost = amount / gold.gold_price  # amount is silver
            user.silver_amount -= amount
            user.gold_amount += total_cost
            new_total_gold = gold.total_gold + calculate_new_supply(amount)

            new_transaction = GoldTransaction(
                total_gold=new_total_gold,
                gold_price=calculate_price(new_total_gold),
                old_gold_price=gold.gold_price,
                user_id=user_id,
                type="+",
            )
            session.add(user)
            session.add(new_transaction)
            await session.commit()
            await session.refresh(new_transaction)
            return GoldListDTO.model_validate(
                new_transaction
            ), UserListDTO.model_validate(user)

    async def sell_gold(self, user_id, amount: float):
        async with sessionmanager.session() as session:
            user = await session.get(User, user_id)
            if not user:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "User does not exist")

            gold = await session.scalar(
                select(GoldTransaction)
                .order_by(GoldTransaction.created_at.desc())
                .limit(1)
            )

            if not gold:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, "Transaction does not exist"
                )

            if user.gold_amount < amount:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "Insufficient gold.")

            total_revenue = gold.gold_price * amount
            user.gold_amount -= amount
            user.silver_amount += total_revenue
            new_gold_amount = gold.total_gold - calculate_new_supply(amount)

            new_transaction = GoldTransaction(
                total_gold=new_gold_amount,
                gold_price=calculate_price(new_gold_amount),
                old_gold_price=gold.gold_price,
                user_id=user_id,
                type="-",
            )
            session.add(user)
            session.add(new_transaction)
            await session.commit()
            await session.refresh(new_transaction)
            return GoldListDTO.model_validate(
                new_transaction
            ), UserListDTO.model_validate(user)
