from sqlalchemy import Column, String, Integer, select, Numeric
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_session import SqlAlchemyBase as Base

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, nullable=False, primary_key=True)
    city = Column(String, nullable=False)
    district = Column(String)
    street = Column(String, nullable=False)
    home = Column(String, nullable=False)
    entrance = Column(String)
    apartment = Column(String)
    intercom = Column(String)
    latitude = Column(Numeric(9, 6), nullable=False)
    longitude = Column(Numeric(9, 6), nullable=False)