from fastapi import APIRouter, Depends, Query
from services import OrderService, get_order_service,OrderItemService,get_order_item_service
from schemas import OrderCreate, OrderUpdate, CustomOrderCreateWithItems,RegularOrderCreateWithItems

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("")
async def create_order(
    data: OrderCreate,
    is_custom: bool = False,
    service: OrderService = Depends(get_order_service)
):
    return await service.create(data, is_custom=is_custom)

@router.post("/custom")
async def create_custom_order_with_items(
    data: CustomOrderCreateWithItems,
    order_service: OrderService = Depends(get_order_service),
    order_item_service: OrderItemService = Depends(get_order_item_service)
):
        order = None

        try:
            order = await order_service.create_order(data.order, is_custom=True)

            items = await order_item_service.create_custom_bulk(
                order.id,
                data.items
            )

            return {
                "order": order,
                "items": items
            }

        except Exception as e:
            if order:
                try:
                    await self.repo.delete(order.id)
                except Exception:
                    pass
            raise


@router.post("/regular")
async def create_regular_order_with_items(
    data: RegularOrderCreateWithItems,
    order_service: OrderService = Depends(get_order_service),
    order_item_service: OrderItemService = Depends(get_order_item_service)
):
        order = None

        try:
            order = await order_service.create_order(data.order, is_custom=False)

            items = await order_item_service.create_regular_bulk(
                order.id,
                data.items
            )

            return {
                "order": order,
                "items": items
            }

        except Exception as e:
            if order:
                try:
                    await self.repo.delete(order.id)
                except Exception:
                    pass
            raise


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