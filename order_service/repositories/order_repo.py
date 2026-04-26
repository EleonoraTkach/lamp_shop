from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends

from models import Order
from .base_repo import BaseRepository
from db import get_session


class OrderRepository(BaseRepository[Order]):
    model = Order

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.db = db

    async def create(self, data: dict) -> Order:
        order = Order(**data)
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        return order

    async def exists_by_number(self, order_number : str, delete_flg: bool|None) -> bool:
        query = select(Order).where(Order.order_number  == order_number )

        if delete_flg is not None:
            query = query.where(Order.is_deleted == delete_flg)


        result = await self.db.execute(query)
        return result.scalar_one_or_none()

async def get_order_repository(
        db: AsyncSession = Depends(get_session),
) -> OrderRepository:
    return OrderRepository(db)