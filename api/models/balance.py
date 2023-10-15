from sqlalchemy import Column, Integer, ForeignKey, Numeric, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.transaction import Transaction

from models.db_session import SqlAlchemyBase as Base

class Balance(Base):
    __tablename__ = "balances"
    id = Column(Integer, primary_key=True, autoincrement=True)
    deliveryman_id = Column(Integer, ForeignKey("deliverymen.id"), nullable=False)
    sum = Column(Numeric(9, 2), nullable=False)

    @classmethod
    async def get_balance_by_deliveryman_id(cls, deliveryman_id: int, session: AsyncSession):
        """
        Get deliveryman's balance by deliveryman id

        :param deliveryman_id: id of deliveryman
        :param session: session
        :return: balance
        :rtype: Balance
        """

        _ = await session.execute(select(cls).where(cls.deliveryman_id == deliveryman_id))
        return _.scalar()
    
    @classmethod
    async def withdraw_money(cls, deliveryman_id: int, sum: int, session: AsyncSession):
        """
        Withdraw money from the deliveryman account

        :param deliveryman_id: id of deliveryman
        :param sum: withdrawal amount
        :param session: session
        """

        if balance := await session.execute(select(cls).where(cls.deliveryman_id == deliveryman_id, cls.sum >= sum)):
            balance.scalar().sum -= sum
            await session.commit()
            await Transaction(sum=sum, deliveryman_id=deliveryman_id, type="withdraw").save(session)
            return True
        return False
    
    @classmethod
    async def recharge(cls, deliveryman_id: int, sum: int, session: AsyncSession):
        """
        Recharge deliveryman balance

        :param deliveryman_id: id of deliveryman
        :param sum: recharge amount
        :param session: session
        """

        _ = await session.execute(update(cls).where(cls.deliveryman_id == deliveryman_id).values(sum = cls.sum + sum))
        await session.commit()
        await Transaction(sum=sum, deliveryman_id=deliveryman_id, type="recharge").save(session)