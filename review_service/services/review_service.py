from exceptions import NotFoundError, ConflictError
from .base_service import BaseService
from repositories import ReviewRepository, get_review_repository
from fastapi import Depends
from .order_service import OrderClient
from .catalog_service import CatalogClient


class ReviewService(BaseService):
    def __init__(self, repo:ReviewRepository, catalog_client, order_client):
        super().__init__(repo)
        self.repo = repo
        self.catalog_client = catalog_client
        self.order_client = order_client

    async def get_by_id(self, id: int, delete_flg:bool | None):
        obj = await super().get_by_id(id,delete_flg)

        if not obj:
            raise NotFoundError("review not found")

        return obj

    async def get_all(self, delete_flg:bool | None, skip: int, limit: int | None):
        obj = await super().get_all(delete_flg,skip,limit)

        if not obj:
            raise NotFoundError("reviews not found")

        return obj

    async def create(self, product_id: int, data):
        exists_product = await self.catalog_client.product_exists(product_id)

        if not exists_product:
            raise NotFoundError(f"Product {product_id} not found")

        exists_order = await self.order_client.order_exists(data.order_number)

        if not exists_order:
            raise NotFoundError(f"Order {data.order_number} not found")

        existing_review = await self.repo.get_by_product_and_order(product_id,data.order_number)

        if existing_review:
            raise ConflictError(f"For this product and order review was created")

        return await self.repo.create(product_id, data.model_dump())

    async def get_by_product(self, product_id: int, delete_flg:bool | None, skip: int, limit: int | None):
        items = await self.repo.get_by_product(product_id, delete_flg, skip, limit)

        return {
            "product_id": product_id,
            "items": items
        }

async def get_review_service(
    repo: ReviewRepository = Depends(get_review_repository),
    catalog_client: CatalogClient = Depends(),
    order_client: OrderClient = Depends()
) -> ReviewService:
    return ReviewService(repo,catalog_client,order_client)