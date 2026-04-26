from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends

from models import Category
from .base_repo import BaseRepository
from db import get_session


class CategoryRepository(BaseRepository[Category]):
    model = Category

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.db = db

    async def create(self, data: dict) -> Category:
        category = Category(**data)
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def exists_by_name(self, name: str, exclude_id: int|None) -> bool:
        query = select(Category.id).where(Category.name == name)

        if exclude_id is not None:
            query = query.where(Category.id != exclude_id)


        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None

async def get_category_repository(
        db: AsyncSession = Depends(get_session),
) -> CategoryRepository:
    return CategoryRepository(db)