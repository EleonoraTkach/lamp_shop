from exceptions import NotFoundError,ConflictError
from .base_service import BaseService
from repositories import OrderItemRepository, get_order_item_repository
from fastapi import Depends
from .catalog_service import CatalogClient


class OrderItemService(BaseService):
    def __init__(self, repo:OrderItemRepository, catalog_client:CatalogClient):
        super().__init__(repo)
        self.repo = repo
        self.catalog_client = catalog_client

    async def get_by_id(self, id: int, delete_flg:bool | None):
        obj = await super().get_by_id(id,delete_flg)

        if not obj:
            raise NotFoundError("orderItem not found")

        return obj

    async def ensure_order_exists(self, order_id: int, delete_flg:bool | None):
        order = await self.repo.order_exists(order_id, delete_flg)

        if not order:
            raise NotFoundError("order not found")

        return order

    async def create_bulk(self, order_id: int, items):
        if not items:
            raise ConflictError("Список товаров пуст")

        await self.ensure_order_exists(order_id, False)

        for item in items:
            exists = await self.catalog_client.product_exists(item.product_id)

            if not exists:
                raise ConflictError(f"Product {item.product_id} not found")

        items = [item.model_dump() for item in items]

        return await self.repo.create_bulk(order_id, items)

    async def get_by_order(self, order_id: int, delete_flg:bool | None, skip: int, limit: int | None):
        await self.ensure_order_exists(order_id, delete_flg=None)

        items = await self.repo.get_by_order(order_id, delete_flg, skip, limit)

        return {
            "order_id": order_id,
            "items": items
        }

async def get_order_item_service(
    repo: OrderItemRepository = Depends(get_order_item_repository),
    catalog_client: CatalogClient = Depends()
) -> OrderItemService:
    return OrderItemService(repo,catalog_client)