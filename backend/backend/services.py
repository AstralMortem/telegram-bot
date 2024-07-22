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

    def bounding_curve_price(self, amount):
        # @amount: new total gold (GOLD TO SUPLY + GOLD TO TRANSACT)
        # @price: gold price
        k = settings.BOUNDING_CURVE_KOEF / settings.INITIAL_GOLD_SUPPLY
        result = settings.INITIAL_GOLD_PRICE * math.exp(
            k * (amount - settings.INITIAL_GOLD_SUPPLY)
        )
        return round_decimal(result, 4)

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
            user.silver_amount = round_decimal(user.silver_amount - amount, 4)
            user.gold_amount = round_decimal(user.gold_amount + total_cost, 4)
            new_total_gold = round_decimal(gold.total_gold + total_cost, 4)

            new_transaction = GoldTransaction(
                total_gold=new_total_gold,
                gold_price=self.bounding_curve_price(new_total_gold),
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

            total_revenue = round_decimal(gold.gold_price * amount, 4)
            user.gold_amount = round_decimal(user.gold_amount - amount, 4)
            user.silver_amount = round_decimal(user.silver_amount + total_revenue, 4)
            new_gold_amount = round_decimal(gold.total_gold - amount, 4)

            new_transaction = GoldTransaction(
                total_gold=new_gold_amount,
                gold_price=self.bounding_curve_price(new_gold_amount),
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
