from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass

class OrderItemBulkCreate(BaseModel):
    items: list[OrderItemCreate]


class OrderItemUpdate(BaseModel):
    quantity: Optional[int]


class OrderItemResponse(OrderItemBase):
    order_id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True