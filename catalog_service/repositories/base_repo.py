from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

T = TypeVar("T")


class BaseRepository(Generic[T]):
    model: Type[T]

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int, delete_flg: bool|None) -> Optional[T]:
        query = select(self.model).where(self.model.id == id)

        if delete_flg is not None:
            query = query.where(self.model.is_deleted == delete_flg)

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, delete_flg: bool|None,skip: int, limit: int | None) -> List[T]:
        query = select(self.model)

        if delete_flg is not None:
            query = query.where(self.model.is_deleted == delete_flg)

        query = query.offset(skip)

        if limit is not None:
            query = query.limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def update(self, id: int, data: dict) -> Optional[T]:
        obj = await self.get_by_id(id, False)
        if not obj:
            return None

        for k, v in data.items():
            setattr(obj, k, v)

        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def soft_delete(self, id: int) -> bool:
        obj = await self.get_by_id(id, None)
        if not obj:
            return False

        obj.is_deleted = True
        await self.db.commit()
        return True
