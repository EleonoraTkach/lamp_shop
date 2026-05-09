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

    async def create_custom_bulk(self, order_id: int, items):
        if not items:
            raise ConflictError("Список товаров пуст")

        await self.ensure_order_exists(order_id, False)
        items_data = []

        for item in items:
            if item.image_url and item.quantity>0:
                items_data.append(item.model_dump())
            else:
                raise ConflictError("Ссылка должна быть и количество товаров больше 0")

        return await self.repo.create_bulk(order_id, items_data)

    async def create_regular_bulk(self, order_id: int, items):
        if not items:
            raise ConflictError("Список товаров пуст")

        await self.ensure_order_exists(order_id, False)

        valid_items = []

        for item in items:
            product = await self.catalog_client.get_product(item.product_id)

            if not product:
                raise ConflictError(f"Product {item.product_id} not found")

            qnt = min(item.quantity, product["quantity"])

            if qnt > 0:
                item.quantity = qnt
                valid_items.append(item)

        if not valid_items:
            raise ConflictError("Нет доступных товаров для добавления")

        items_data = [item.model_dump() for item in valid_items]

        for item in valid_items:
            product = await self.catalog_client.get_product(item.product_id)

            new_quantity = product["quantity"] - item.quantity

            await self.catalog_client.update_quantity(
                item.product_id,
                new_quantity
            )

        return await self.repo.create_bulk(order_id, items_data)

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