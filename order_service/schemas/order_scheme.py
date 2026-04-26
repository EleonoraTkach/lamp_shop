from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrderBase(BaseModel):
    phone_number: str
    user_full_name: str
    preorder_id: Optional[int] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    phone_number: Optional[str] = None
    user_full_name: Optional[str] = None
    status: Optional[str] = None
    preorder_id: Optional[int] = None
    total_cost: Optional[float] = None


class OrderResponse(OrderBase):
    id: int
    order_number: str
    status: str
    total_cost: float
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True