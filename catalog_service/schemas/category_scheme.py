from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: Optional[str]


class CategoryOut(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    is_deleted: bool