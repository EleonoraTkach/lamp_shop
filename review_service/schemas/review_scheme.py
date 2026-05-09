from pydantic import BaseModel
from datetime import datetime


class ReviewCreate(BaseModel):
    order_number: str
    score: int
    description: str | None = None


class ReviewUpdate(BaseModel):
    score: int | None = None
    description: str | None = None


class ReviewResponse(BaseModel):
    id: int
    product_id: int
    order_number: str
    score: int
    description: str | None
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True