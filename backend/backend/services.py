from typing import Any
from fastapi import HTTPException, status
from sqlalchemy import select
from db.connect import sessionmanager
from db.models import GoldTransaction, User
from db.schemas import GoldListDTO, Pagination, UserAddDTO, UserListDTO
from config import settings


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
                select(GoldTransaction).order_by(GoldTransaction.created_at).limit(1)
            )
            instance = await session.scalar(statement)
            if not instance:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, "Transaction does not exists"
                )
            return GoldListDTO.model_validate(instance)

    def bounding_curve_price(self, x):
        return (
            settings.CURVE_KOEF_A * x**2
            + settings.CURVE_KOEF_B * x
            + settings.CURVE_KOEF_C
        )

    async def buy_gold(self, user_id, amount):
        async with sessionmanager.session() as session:
            user = await session.get(User, user_id)
            if not user:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "User does not exist")

            gold = await session.scalar(
                select(GoldTransaction).order_by(GoldTransaction.created_at).limit(1)
            )

            if not gold:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, "Transaction does not exist"
                )

            current_price = self.bounding_curve_price(gold.total_gold)
            total_cost = current_price * amount

            if user.silver_amount < total_cost:
                raise HTTPException(
                    status.HTTP_405_METHOD_NOT_ALLOWED, "Insufficient silver."
                )
            user.silver_amount -= total_cost
            user.gold_amount += amount
            gold.total_gold += amount
            gold.gold_price = self.bounding_curve_price(gold.total_gold)
            session.add(user)
            session.add(gold)
            await session.commit()
            await session.refresh(gold)
            return GoldListDTO.model_validate(gold)

    async def sell_gold(self, user_id, amount):
        async with sessionmanager.session() as session:
            user = await session.get(User, user_id)
            if not user:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "User does not exist")

            gold = await session.scalar(
                select(GoldTransaction).order_by(GoldTransaction.created_at).limit(1)
            )

            if not gold:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, "Transaction does not exist"
                )

            current_price = self.bounding_curve_price(gold.total_gold)
            total_revenue = current_price * amount

            if user.gold_amount < total_revenue:
                raise HTTPException(
                    status.HTTP_405_METHOD_NOT_ALLOWED, "Insufficient gold."
                )
            user.gold_amount -= amount
            user.silver_amount += total_revenue
            gold.total_gold -= amount
            gold.gold_price = self.bounding_curve_price(gold.total_gold)
            session.add(user)
            session.add(gold)
            await session.commit()
            await session.refresh(gold)
            return GoldListDTO.model_validate(gold)
