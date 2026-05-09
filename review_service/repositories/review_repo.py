from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends

from models import Review
from .base_repo import BaseRepository
from db import get_session


class ReviewRepository(BaseRepository[Review]):
    model = Review

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.db = db

    async def create(self, product_id: int, data: dict) -> Review:
        review = Review(product_id=product_id,**data)
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return review

    async def get_by_product(self, product_id: int, delete_flg:bool | None, skip: int, limit: int | None):
        query = select(Review).where(Review.product_id == product_id)

        if delete_flg is not None:
            query = query.where(Review.is_deleted == delete_flg)

        query = query.offset(skip)

        if limit is not None:
            query = query.limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_product_and_order(self, product_id: int, order_number:str):
        query = select(Review).where(
            Review.product_id == product_id,
            Review.order_number == order_number,
            Review.is_deleted == False
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

async def get_review_repository(
        db: AsyncSession = Depends(get_session),
) -> ReviewRepository:
    return ReviewRepository(db)