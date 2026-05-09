from fastapi import APIRouter, Depends, status

from schemas import ReviewCreate, ReviewUpdate
from services import ReviewService, get_review_service

router = APIRouter(prefix="", tags=["Reviews"])


@router.get("/reviews/{id}")
async def get_review(
    id: int,
    delete_flg: bool | None = None,
    service: ReviewService = Depends(get_review_service),
):
    return await service.get_by_id(id, delete_flg)


@router.post("/products/{product_id}/reviews", status_code=status.HTTP_201_CREATED)
async def create_review(
    product_id: int,
    data: ReviewCreate,
    service: ReviewService = Depends(get_review_service),
):
    product = await service.create(product_id, data)
    return {"id": product.id}


@router.patch("/reviews/{id}")
async def update_review(
    id: int,
    data: ReviewUpdate,
    service: ReviewService = Depends(get_review_service),
):
    return await service.update(id, data)


@router.delete("/reviews/{id}")
async def delete_review(
    id: int,
    service: ReviewService = Depends(get_review_service),
):
    await service.soft_delete(id)
    return {"status": "deleted"}


@router.get("/products/{product_id}/reviews")
async def get_reviews_by_product(
    product_id: int,
    skip: int = 0,
    limit: int = 100,
    delete_flg: bool | None = None,
    service: ReviewService = Depends(get_review_service),
):
    return await service.get_by_product(product_id, delete_flg,skip, limit)