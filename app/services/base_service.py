from uuid import UUID
from fastapi import HTTPException, status

from exceptions import (
    NotFoundError,
    ConflictError
)

class BaseService:
    def __init__(self, repo):
        self.repo = repo

    async def get_all(self, delete_flg:bool | None, skip: int, limit: int | None):
        res = await self.repo.get_all(delete_flg, skip, limit)
        if not res:
            raise NotFoundError(f"Объекты не найден")
        return res

    async def get_by_id(self, id: int, delete_flg:bool | None):
        res = await self.repo.get_by_id(id, delete_flg)
        if res is None:
            raise NotFoundError(f"Объект не найден")
        return res


    async def update(self, id: int, in_data):
        await self.get_by_id(id, False)
        update_dict = {k: v for k, v in in_data.model_dump().items() if v is not None}
        if not update_dict:
            raise UpdateEmptyError()

        return await self.repo.update(id, update_dict)

    async def soft_delete(self, id: int) -> bool:
        obj = await self.get_by_id(id, None)

        if obj.is_deleted:
            raise ConflictError("Объект уже удалён (soft delete)")

        return await self.repo.soft_delete(id)

    async def hard_delete(self, id: int) -> bool:
        await self.get_by_id(id, None)
        res = await self.repo.hard_delete(id)
        return res