from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_bearer import JWTBearer, JWTHeader
from models.order import Order
from models.db_session import get_session
from pydantic_models.order import OrderModel, OrderIdIn
from descriptions.deliveryman import *

router = APIRouter()

@router.get("/order/{order_id}", summary="Get order by id", operation_id="get-order-by-id",
            description=get_order_by_id_description, response_model=OrderModel)
async def get_order_by_id(order_id: int, session: AsyncSession = Depends(get_session), token: JWTHeader = Depends(JWTBearer())):
    if order := await Order.get_order_by_id_for_deliveryman(order_id, session, token.deliveryman_id):
        return OrderModel.model_validate(order)
    return Response(status_code=404)

@router.get("/all", summary="Get orders", operation_id="get-orders",
            description=get_orders_description, response_model=list[OrderModel])
async def get_orders(session: AsyncSession = Depends(get_session), token: JWTHeader = Depends(JWTBearer())):
    if orders := await Order.get_all_orders(token.deliveryman_id, session):
        return [
            OrderModel.model_validate(order)
            for order in orders
        ]
    return Response(status_code=404)

@router.get("/{order_status}", summary="Get orders by status", operation_id="get-orders-by-status",
            description=get_orders_by_status_description, response_model=list[OrderModel])
async def get_orders(order_status: str, session: AsyncSession = Depends(get_session), token: JWTHeader = Depends(JWTBearer())):
    if orders := await Order.get_orders_by_status(order_status, session, token.deliveryman_id):
        return [
            OrderModel.model_validate(order)
            for order in orders
        ]
    return Response(status_code=404)

@router.post("/take-order", summary="Assign deliveryman to order", operation_id="assign-deliveryman-to-order",
             description=assign_deliveryman_to_order_description, response_class=Response)
async def assign_deliveryman(order: OrderIdIn, session: AsyncSession = Depends(get_session),
                            token: JWTHeader = Depends(JWTBearer())):
    resp = await Order.assign_deliveryman(order.id, token.deliveryman_id, session)
    if resp:
        return Response(status_code=202)
    return Response(status_code=404)

@router.post("/complete/{order_id}", summary="Complete order", operation_id="complete-order",
             description=complete_order_description, response_class=Response)
async def complete_order(order_id: int, session: AsyncSession=Depends(get_session), token: JWTHeader=Depends(JWTBearer())):
    resp = await Order.complete_order(order_id, token.deliveryman_id, session)
    if resp:
        return Response(status_code=202)
    return Response(status_code=404)