from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrderItemBase(BaseModel):
    quantity: int


class RegularOrderItemCreate(OrderItemBase):
    product_id: int

class CustomOrderItemCreate(OrderItemBase):
    image_url: str

class RegularOrderItemBulkCreate(BaseModel):
    items: list[RegularOrderItemCreate]

class CustomOrderItemBulkCreate(BaseModel):
    items: list[CustomOrderItemCreate]


class OrderItemUpdate(BaseModel):
    quantity: Optional[int]


class RegularOrderItemResponse(RegularOrderItemCreate):
    order_id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True

class CustomOrderItemResponse(CustomOrderItemCreate):
    order_id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True