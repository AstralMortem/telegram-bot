from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class UserAddDTO(BaseModel):
    tg_id: str
    username: str
    silver_amount: float = 1000
    gold_amount: float = 0
    is_active: bool = True
    created_at: datetime | None = None


class UserListDTO(UserAddDTO):
    id: UUID


class GoldAddDTO(BaseModel):
    total_gold: float = 1_000_000_000
    gold_price: float = 1
    user_id: UUID | None = None
    created_at: datetime | None = None


class GoldListDTO(GoldAddDTO):
    id: UUID


class Pagination(BaseModel):
    limit: int
    offset: int
