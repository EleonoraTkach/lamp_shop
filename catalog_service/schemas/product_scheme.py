from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import datetime


class ProductCreate(BaseModel):
    name: str
    description: str
    price: condecimal(max_digits=8, decimal_places=2)
    quantity: int


class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[condecimal(max_digits=8, decimal_places=2)]
    quantity: Optional[int]


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