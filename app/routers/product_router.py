from fastapi import APIRouter, Depends, status

from schemas import ProductCreate, ProductUpdate
from services import ProductService, get_product_service

router = APIRouter(prefix="", tags=["Products"])


@router.get("/products/{id}")
async def get_product(
    id: int,
    delete_flg: bool | None = None,
    service: ProductService = Depends(get_product_service),
):
    return await service.get_by_id(id, delete_flg)


@router.post("/categories/{category_id}/products", status_code=status.HTTP_201_CREATED)
async def create_product(
    category_id: int,
    data: ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    product = await service.create(category_id, data)
    return {"id": product.id}


@router.patch("/products/{id}")
async def update_product(
    id: int,
    data: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    return await service.update(id, data)


@router.delete("/products/{id}")
async def delete_product(
    id: int,
    service: ProductService = Depends(get_product_service),
):
    await service.soft_delete(id)
    return {"status": "deleted"}


@router.get("/categories/{category_id}/products")
async def get_products_by_category(
    category_id: int,
    skip: int = 0,
    limit: int = 100,
    delete_flg: bool | None = None,
    service: ProductService = Depends(get_product_service),
):
    return await service.get_by_category(category_id, delete_flg,skip, limit)