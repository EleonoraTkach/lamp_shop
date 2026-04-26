from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends

from models import Product, Category
from .base_repo import BaseRepository
from db import get_session


class ProductRepository(BaseRepository[Product]):
    model = Product

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.db = db

    async def create(self, category_id: int, data: dict) -> Product:
        product = Product(**data, category_id=category_id)
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def get_by_category(self, category_id: int, delete_flg:bool | None, skip: int, limit: int | None):
        query = select(Product).where(Product.category_id == category_id)

        if delete_flg is not None:
            query = query.where(Product.is_deleted == delete_flg)

        query = query.offset(skip)

        if limit is not None:
            query = query.limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def category_exists(self, category_id: int, delete_flg: bool|None) -> bool:
        query = select(Category.id).where(Category.id == category_id)

        if delete_flg is not None:
            query = query.where(Category.is_deleted == delete_flg)

        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None

async def get_product_repository(
        db: AsyncSession = Depends(get_session),
) -> ProductRepository:
    return ProductRepository(db)