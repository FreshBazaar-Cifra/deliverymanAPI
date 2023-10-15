from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_bearer import JWTBearer, JWTHeader
from models.db_session import get_session
from pydantic_models.balance import BalanceModel
from descriptions.deliveryman import *
from models.balance import Balance
from pydantic_models.transaction import TransactionModel
from models.transaction import Transaction

router = APIRouter()

@router.get("/", summary="Get deliveryman's balance", operation_id="get-deliveryman's balance",
            description=get_deliverymans_balance_description, response_model=BalanceModel)
async def get_deliverymans_balance(session: AsyncSession = Depends(get_session), token: JWTHeader = Depends(JWTBearer())):
    if balance := await Balance.get_balance_by_deliveryman_id(token.deliveryman_id, session):
        return BalanceModel.model_validate(balance)
    return Response(status_code=404)

@router.get("/history", summary="Get deliveryman transactions history", operation_id="get-deliveryman-transactions-history",
            description=get_deliveryman_transactions_history_description, response_model=list[TransactionModel])
async def get_deliveryman_transactions_history(session: AsyncSession = Depends(get_session), token: JWTHeader = Depends(JWTBearer())):
    if history := await Transaction.get_transactions_by_deliveryman_id(token.deliveryman_id, session):
        return [
            TransactionModel.model_validate(history_item)
            for history_item in history
        ]
    return Response(status_code=404)

@router.post("/withdraw", summary="Withdraw money from the deliveryman account", operation_id="withdraw-money-from-the-deliveryman-account", 
             description=withdraw_money_description, response_class=Response)
async def withdraw_money(sum: BalanceModel, session: AsyncSession=Depends(get_session), token: JWTHeader = Depends(JWTBearer())):
    resp = await Balance.withdraw_money(token.deliveryman_id, sum.sum, session)
    if resp:
        return Response(status_code=202)
    return Response(status_code=404)