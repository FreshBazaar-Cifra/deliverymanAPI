from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.db_session import SqlAlchemyBase as Base


class Position(Base):
    __tablename__ = 'positions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product = relationship("Product", lazy="selectin")
    count = Column(Integer, default=1, nullable=False)
