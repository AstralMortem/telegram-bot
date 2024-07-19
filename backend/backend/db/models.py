from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Float, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    pass


class User(BaseModel):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4())
    tg_id: Mapped[str] = mapped_column(unique=True, index=True)
    username: Mapped[str]
    silver_amount: Mapped[float] = mapped_column(Float(precision=2), default=1000)
    gold_amount: Mapped[float] = mapped_column(Float(precision=2), default=0)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    is_active: Mapped[bool] = mapped_column(default=True)


class GoldTransaction(BaseModel):
    __tablename__ = "gold_transactions"
    id: Mapped[UUID] = mapped_column(default=uuid4(), primary_key=True, index=True)
    total_gold: Mapped[Float] = mapped_column(Float(precision=2), default=1_000_000_000)
    gold_price: Mapped[Float] = mapped_column(Float(precision=2), default=1)
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
