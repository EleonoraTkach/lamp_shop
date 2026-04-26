from fastapi import APIRouter, Depends, status

from schemas import CategoryCreate, CategoryUpdate
from services import CategoryService, get_category_service

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
):
    category = await service.create(data)
    return {"id": category.id}


@router.get("")
async def get_categories(
    skip: int = 0,
    limit: int = 100,
    delete_flg: bool | None = None,
    service: CategoryService = Depends(get_category_service),
):
    res = await service.get_all(delete_flg,skip, limit)
    return res


@router.get("/{id}")
async def get_category(
    id: int,
    delete_flg: bool | None = None,
    service: CategoryService = Depends(get_category_service),
):
    res = await service.get_by_id(id, delete_flg)
    return res


@router.put("/{id}")
async def update_category(
    id: int,
    data: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
):
    res = await service.update_category(id, data)
    return res


@router.delete("/{id}")
async def delete_category(
    id: int,
    service: CategoryService = Depends(get_category_service),
):
    await service.soft_delete(id)
    return {"status": "deleted"}