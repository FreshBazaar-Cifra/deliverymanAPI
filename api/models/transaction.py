from sqlalchemy import DateTime, Integer, Column, ForeignKey, String, select
from sqlalchemy.ext.asyncio import AsyncSession
import datetime

from models.db_session import SqlAlchemyBase as Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.datetime.now, nullable=False)
    sum = Column(Integer, nullable=False)
    deliveryman_id = Column(Integer, ForeignKey("deliverymen.id"), nullable=False)
    type = Column(String, nullable=False)

    @classmethod
    async def get_transactions_by_deliveryman_id(cls, deliveryman_id: int, session: AsyncSession):
        """
        Get history of transactions for deliveryman

        :param deliveryman_id: id of deliveryman
        :param session: session
        :return: list[Transaction]
        :rtype: list[Transaction]
        """

        _ = await session.execute(select(cls).where(cls.deliveryman_id == deliveryman_id))
        return _.scalars().all()