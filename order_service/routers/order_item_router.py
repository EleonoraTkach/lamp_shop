from fastapi import APIRouter, Depends
from services import OrderItemService, get_order_item_service
from schemas import RegularOrderItemBulkCreate,CustomOrderItemBulkCreate, OrderItemUpdate

router = APIRouter(prefix="/orders", tags=["Order Items"])


@router.post("/{id}/items/regular")
async def add_item(
    id: int,
    data: RegularOrderItemBulkCreate,
    service: OrderItemService = Depends(get_order_item_service)
):
    return await service.create_regular_bulk(id, data.items)

@router.post("/{id}/items/custom")
async def add_item(
    id: int,
    data: CustomOrderItemBulkCreate,
    service: OrderItemService = Depends(get_order_item_service)
):
    return await service.create_custom_bulk(id, data.items)

@router.get("/{id}/items")
async def get_by_order(
    id: int,
    skip: int = 0,
    limit: int = 100,
    delete_flg: bool | None = None,
    service: OrderItemService = Depends(get_order_item_service)
):
    return await service.get_by_order(id,delete_flg,skip,limit)


@router.patch("/items/{id}")
async def update_item(
    id: int,
    data: OrderItemUpdate,
    service: OrderItemService = Depends(get_order_item_service)
):
    return await service.update(id,data)


@router.delete("/items/{id}")
async def delete_item(
    id: int,
    service: OrderItemService = Depends(get_order_item_service)
):
    return await service.soft_delete(id)