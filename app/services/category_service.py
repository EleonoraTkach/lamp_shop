from exceptions import NotFoundError, ConflictError
from .base_service import BaseService
from repositories import CategoryRepository,get_category_repository
from fastapi import Depends


class CategoryService(BaseService):
    def __init__(self, repo: CategoryRepository):
        super().__init__(repo)
        self.repo = repo

    async def create(self, data):
        if await self.repo.exists_by_name(data.name, exclude_id=None):
            raise ConflictError("This category already exists")

        return await self.repo.create(data.model_dump())

    async def get_by_id(self, id: int,delete_flg:bool | None):
        obj = await super().get_by_id(id,delete_flg)

        if not obj:
            raise NotFoundError("category not found")

        return obj

    async def update_category(self, id:int, data):
        if data.name:
            if await self.repo.exists_by_name(data.name, exclude_id=id):
                raise ConflictError("Category with this name already exists")

        return await super().update(id, data)

    async def get_all(self, delete_flg:bool | None, skip: int, limit: int | None):
        res = await super().get_all(delete_flg,skip,limit)

        if not res:
            raise NotFoundError("category not found")

        return res


async def get_category_service(
    repo: CategoryRepository = Depends(get_category_repository)
) -> CategoryService:
    return CategoryService(repo)