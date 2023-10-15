import datetime

from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, select, Table
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from models.deliveryman import Deliveryman
from models.address import Address
from models.balance import Balance
from sqlalchemy import text
from sqlalchemy import or_, and_

from models.db_session import SqlAlchemyBase as Base



orders_to_positions = Table(
    "orders_to_positions",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id")),
    Column("position_id", ForeignKey("positions.id")),
)


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", lazy="selectin")
    positions = relationship("Position", secondary=orders_to_positions, lazy="selectin")
    date = Column(DateTime, default=datetime.datetime.now, nullable=False)
    status = Column(String, default="created", nullable=False)
    deliveryman_id = Column(Integer, ForeignKey("deliverymen.id"))
    deliveryman = relationship("Deliveryman", lazy="selectin")
    price = Column(Numeric(10, 2), nullable=False)
    delivery_price = Column(Numeric(7, 2), nullable=False)
    promocode_id = Column(Integer, ForeignKey("promocodes.id"))
    promocode = relationship("Promocode", lazy="selectin")
    total = Column(Numeric(11, 2), nullable=False)
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)
    address = relationship("Address", lazy="selectin")
    market_id = Column(Integer, ForeignKey("markets.id"), nullable=False)
    market = relationship("Market", lazy="selectin")

    @classmethod
    async def get_orders_by_user(cls, user_id: int, session: AsyncSession):
        """
        Get all orders of user

        :param user_id: id of user
        :param session: session
        :return: list of orders
        :rtype: list[Order]
        """

        _ = await session.execute(select(cls).where(cls.user_id == user_id))
        return _.scalars().all()

    @classmethod
    async def get_order_by_id(cls, order_id: int, user_id: int, session: AsyncSession):
        """
        Get order by id

        :param order_id: id of order
        :param user_id: id of user
        :param session: session
        :return: Order
        :rtype: Order
        """

        _ = await session.execute(select(cls).where(cls.id == order_id, cls.user_id == user_id))
        return _.scalar()
    
    @classmethod
    async def get_orders_by_status(cls, order_status: str, session: AsyncSession, deliveryman_id: int):
        """
        Get list of orders by status

        :param order_status: status of order
        :param session: session
        :return: List[Order]
        :rtype: List[Order]
        """
        _ = await session.execute(select(cls).join(Address, Address.id == cls.address_id).join(Deliveryman, Deliveryman.id == deliveryman_id).where(cls.status == order_status, Address.city == Deliveryman.city))
        return _.scalars().all()
    
    @classmethod
    async def get_order_by_id_for_deliveryman(cls, order_id: int, session: AsyncSession, deliveryman_id: int):
        """
        Get order by id

        :param order_id: id of order
        :param session: session
        :param deliveryman_id: id of deliveryman
        :return: Order
        :rtype: Order
        """
        print(order_id, deliveryman_id)
        _ = await session.execute(select(cls).join(Address, cls.address_id==Address.id).join(Deliveryman, Deliveryman.id == deliveryman_id).where(or_(and_(cls.id == order_id, cls.status == "paid", Address.city == Deliveryman.city), and_(cls.deliveryman_id == deliveryman_id, cls.id == order_id))))
        return _.scalar()
    
    @classmethod
    async def assign_deliveryman(cls, order_id: int, deliveryman_id: int, session: AsyncSession):
        """
        assign deliveryman to order

        :param order_id: id of order
        :param deliveryman_id: id of deliveryman
        :param session: session
        :return: None
        """

        if deliveryman := await Deliveryman.get_deliveryman_by_id(deliveryman_id, session):
            query = text(
                "UPDATE orders AS o "
                "SET deliveryman_id = :deliveryman_id, status = 'confirmed' "
                "FROM addresses AS a "
                "WHERE o.id = :id AND o.status = 'paid' AND a.id = o.address_id AND a.city = :city"
            )
            await session.execute(query, {
                "deliveryman_id": deliveryman_id,
                "city": deliveryman.city,
                "id": order_id
            })
            await session.commit()
            _ = await session.execute(select(cls).where(cls.id == order_id))
            if _.scalar().deliveryman_id == deliveryman_id:
                return True
            else:
                return False
        return False
    
    @classmethod
    async def complete_order(cls, order_id: int, deliveryman_id: int, session: AsyncSession):
        """
        Complete order

        :param deliveryman_id: id of deliveryman
        :param session: session
        """

        if order := await session.execute(select(cls).where(cls.deliveryman_id==deliveryman_id, cls.id==order_id)):
            order = order.scalar()
            await Balance.recharge(deliveryman_id, order.delivery_price, session)
            order.status = "delivered"
            await session.commit()
            return True
        return False
    
    @classmethod
    async def get_all_orders(cls, deliveryman_id: int, session: AsyncSession):
        """
        Get all orders special for Kirill Romanyuk

        :param deliveryman_id: id of deliveryman
        :param session: session
        :return: list[Order]
        :rtype: list[Order]
        """

        _ = await session.execute(select(cls).join(Address, Address.id == cls.address_id).join(Deliveryman, Deliveryman.id == deliveryman_id).where(Address.city == Deliveryman.city))
        return _.scalars().all()