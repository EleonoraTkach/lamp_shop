from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import datetime


class ProductCreate(BaseModel):
    name: str
    description: str
    price: condecimal(max_digits=8, decimal_places=2)
    quantity: int


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: condecimal(max_digits=8, decimal_places=2) | None = None
    quantity: int | None = None


class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: condecimal(max_digits=10, decimal_places=2)
    quantity: int
    category_id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool