from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, ARRAY, Numeric, select
from sqlalchemy.ext.asyncio import AsyncSession

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