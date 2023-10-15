from sqlalchemy import Column, Integer, SmallInteger, String

from models.db_session import SqlAlchemyBase as Base


class Promocode(Base):
    __tablename__ = 'promocodes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sale = Column(SmallInteger, nullable=False)
    count = Column(Integer, nullable=False)
    code = Column(String, nullable=False)
