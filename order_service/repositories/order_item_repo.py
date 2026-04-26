from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends

from models import OrderItem, Order
from .base_repo import BaseRepository
from db import get_session
from typing import List


class OrderItemRepository(BaseRepository[OrderItem]):
    model = OrderItem

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.db = db

    async def create(self, order_id: int, data: dict) -> OrderItem:
        orderItem = OrderItem(**data, order_id=order_id)
        self.db.add(orderItem)
        await self.db.commit()
        await self.db.refresh(orderItem)
        return orderItem

    async def create_bulk(self, order_id: int, data: List[dict]) -> List[OrderItem]:
        items = [
            OrderItem(**item, order_id=order_id)
            for item in data
        ]

        self.db.add_all(items)
        await self.db.commit()

        for item in items:
            await self.db.refresh(item)

        return items

    async def get_by_order(self, order_id: int, delete_flg:bool | None, skip: int, limit: int | None):
        query = select(OrderItem).where(OrderItem.order_id == order_id)

        if delete_flg is not None:
            query = query.where(OrderItem.is_deleted == delete_flg)

        query = query.offset(skip)

        if limit is not None:
            query = query.limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def order_exists(self, order_id: int, delete_flg: bool|None) -> bool:
        query = select(Order.id).where(Order.id == order_id)

        if delete_flg is not None:
            query = query.where(Order.is_deleted == delete_flg)

        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None

async def get_order_item_repository(
        db: AsyncSession = Depends(get_session),
) -> OrderItemRepository:
    return OrderItemRepository(db)