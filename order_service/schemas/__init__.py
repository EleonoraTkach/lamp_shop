from pydantic import BaseModel

from .order_item_scheme import (
    CustomOrderItemResponse,
    CustomOrderItemCreate,
    CustomOrderItemBulkCreate,
    RegularOrderItemResponse,
    RegularOrderItemCreate,
    RegularOrderItemBulkCreate,
    OrderItemUpdate
)
from .order_scheme import OrderCreate,OrderUpdate,OrderResponse

class CustomOrderCreateWithItems(BaseModel):
    order: OrderCreate
    items: list[CustomOrderItemCreate]

class RegularOrderCreateWithItems(BaseModel):
    order: OrderCreate
    items: list[RegularOrderItemCreate]