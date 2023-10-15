from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.types import Decimal
from pydantic_models.address import DeliveryAddress
from pydantic_models.place import DeliveryMarketModel
from pydantic_models.position import DeliveryPosition


class DeliverymanModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    reg_date: str
    phone: str
    city: str

    @field_validator('reg_date', mode='before')
    @classmethod
    def format_date_of_taking(cls, value):
        if value and isinstance(value, datetime):
            return value.isoformat(sep=' ', timespec='seconds')

class OrderModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: str
    status: str
    price: float
    delivery_price: float
    positions: list[DeliveryPosition]
    market: DeliveryMarketModel
    address: DeliveryAddress

    @field_validator('date', mode='before')
    @classmethod
    def format_date_of_taking(cls, value) -> str:
        if value and isinstance(value, datetime):
            return value.isoformat(sep=' ', timespec='seconds')

class OrderIdIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
