from fastapi import APIRouter, Depends
from services import OrderItemService, get_order_item_service
from schemas import OrderItemBulkCreate, OrderItemUpdate

router = APIRouter(prefix="/orders", tags=["Order Items"])


@router.post("/{id}/items")
async def add_item(
    id: int,
    data: OrderItemBulkCreate,
    service: OrderItemService = Depends(get_order_item_service)
):
    return await service.create_bulk(id, data.items)


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