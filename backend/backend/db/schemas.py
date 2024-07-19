from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class UserAddDTO(BaseModel):
    id: int
    username: str
    silver_amount: float = 1000
    gold_amount: float = 0
    is_active: bool = True
    created_at: datetime | None = None
    image_url: str | None = None
    model_config = ConfigDict(from_attributes=True)


class UserListDTO(UserAddDTO):
    pass


class GoldAddDTO(BaseModel):
    total_gold: float = 1_000_000_000
    gold_price: float = 1
    user_id: UUID | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class GoldListDTO(GoldAddDTO):
    id: UUID


class Pagination(BaseModel):
    limit: int | None = None
    offset: int | None = None
