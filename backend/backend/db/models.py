from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import ForeignKey, func, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from ..config import settings


class BaseModel(DeclarativeBase):
    pass


class User(BaseModel):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, unique=True, index=True
    )
    username: Mapped[str]
    silver_amount: Mapped[float] = mapped_column(default=1000)
    gold_amount: Mapped[float] = mapped_column(default=0)
    image_url: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    is_active: Mapped[bool] = mapped_column(default=True)


class GoldTransaction(BaseModel):
    __tablename__ = "gold_transactions"
    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True, index=True)
    total_gold: Mapped[float] = mapped_column(default=settings.INITIAL_GOLD_SUPPLY)
    gold_price: Mapped[float] = mapped_column(default=settings.INITIAL_GOLD_PRICE)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    type: Mapped[str] = mapped_column(default="+")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
