from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_bearer import JWTBearer, JWTHeader
from models.deliveryman import Deliveryman
from models.db_session import get_session
from pydantic_models.order import DeliverymanModel
from descriptions.deliveryman import *

router = APIRouter()

@router.get("/", summary="Get deliveryman by id", operation_id="get-deliveryman-by-id",
             description=get_deliveryman_by_id_description, response_model=DeliverymanModel)
async def get_user(session: AsyncSession = Depends(get_session), 
                   token: JWTHeader = Depends(JWTBearer())):
    if deliveryman := await Deliveryman.get_deliveryman_by_id(token.deliveryman_id, session):
        return DeliverymanModel.model_validate(deliveryman)
    return Response(status_code=404)