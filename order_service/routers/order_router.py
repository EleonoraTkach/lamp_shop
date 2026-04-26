from fastapi import APIRouter, Depends, Query
from services import OrderService, get_order_service
from schemas import OrderCreate, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("")
async def create_order(
    data: OrderCreate,
    service: OrderService = Depends(get_order_service)
):
    return await service.create(data)


@router.get("/{id}")
async def get_order(
    id: int,
    delete_flg: bool | None = None,
    service: OrderService = Depends(get_order_service)
):
    return await service.get_by_id(id, delete_flg)



@router.patch("/{id}")
async def update_order(
    id: int,
    data: OrderUpdate,
    service: OrderService = Depends(get_order_service)
):
    return await service.update(id, data)


@router.delete("/{id}")
async def delete_order(
    id: int,
    service: OrderService = Depends(get_order_service)
):
    return await service.soft_delete(id)


# 2.3.6 GET /orders/track?orderNumber=XXX
@router.get("/track/{orderNumber}")
async def track_order(
    orderNumber: str,
    delete_flg:bool | None  = None,
    service: OrderService = Depends(get_order_service)
):
    return await service.get_by_order_number(orderNumber,delete_flg)