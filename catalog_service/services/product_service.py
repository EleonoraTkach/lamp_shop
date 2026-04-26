from exceptions import NotFoundError
from .base_service import BaseService
from repositories import ProductRepository, get_product_repository
from fastapi import Depends


class ProductService(BaseService):
    def __init__(self, repo:ProductRepository):
        super().__init__(repo)
        self.repo = repo

    async def get_by_id(self, id: int, delete_flg:bool | None):
        obj = await super().get_by_id(id,delete_flg)

        if not obj:
            raise NotFoundError("product not found")

        return obj

    async def ensure_category_exists(self, category_id: int, delete_flg:bool | None):
        category = await self.repo.category_exists(category_id, delete_flg)

        if not category:
            raise NotFoundError("Category not found")

        return category

    async def create(self, category_id: int, data):
        await self.ensure_category_exists(category_id, delete_flg=False)

        return await self.repo.create(category_id, data.model_dump())

    async def get_by_category(self, category_id: int, delete_flg:bool | None, skip: int, limit: int | None):
        await self.ensure_category_exists(category_id, delete_flg=None)

        items = await self.repo.get_by_category(category_id, delete_flg, skip, limit)

        return {
            "category_id": category_id,
            "items": items
        }

async def get_product_service(
    repo: ProductRepository = Depends(get_product_repository)
) -> ProductService:
    return ProductService(repo)