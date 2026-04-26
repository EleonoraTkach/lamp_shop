from exceptions import NotFoundError, ConflictError
from .base_service import BaseService
from repositories import OrderRepository,get_order_repository
from fastapi import Depends


class OrderService(BaseService):
    def __init__(self, repo: OrderRepository):
        super().__init__(repo)
        self.repo = repo

    async def create(self, data):

        return await self.repo.create(data.model_dump())

    async def get_by_id(self, id: int,delete_flg:bool | None):
        obj = await super().get_by_id(id,delete_flg)

        if not obj:
            raise NotFoundError("order not found")

        return obj

    async def get_all(self, delete_flg:bool | None, skip: int, limit: int | None):
        res = await super().get_all(delete_flg,skip,limit)

        if not res:
            raise NotFoundError("order not found")

        return res

    async def get_by_order_number(self, orderNumber: str, delete_flg:bool | None):
        obj = await self.repo.exists_by_number(orderNumber,delete_flg)

        if not obj:
            raise NotFoundError("order not found")

        return obj


async def get_order_service(
    repo: OrderRepository = Depends(get_order_repository)
) -> OrderService:
    return OrderService(repo)