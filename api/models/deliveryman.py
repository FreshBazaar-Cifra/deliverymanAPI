import datetime

from sqlalchemy import Column, Integer, String, DateTime, select
from sqlalchemy.ext.asyncio import AsyncSession


from models.db_session import SqlAlchemyBase as Base


class Deliveryman(Base):
    __tablename__ = 'deliverymen'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    reg_date = Column(DateTime, default=datetime.datetime.now)
    phone = Column(String)
    city = Column(String)

    @classmethod
    async def get_deliveryman_by_id(cls, deliveryman_id: int, session: AsyncSession):
        """
        Get delivery man by id

        :param deliveryman_id: id of deliveryman
        :param session: session
        :return: deliveryman
        :rtype: Deliveryman
        """

        _ = await session.execute(select(cls).where(cls.id == deliveryman_id))
        return _.scalar()