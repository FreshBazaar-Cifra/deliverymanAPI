from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.types import Decimal
from pydantic_models.address import DeliveryAddress
from pydantic_models.place import DeliveryMarketModel


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


class PromocodeModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sale: int
    code: int


class PromocodeCheckIn(BaseModel):
    code: str
    price: float


class PromocodeCheckOut(BaseModel):
    price: float


class OrderModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: str
    status: str
    price: float
    delivery_price: float
    market: DeliveryMarketModel
    address: DeliveryAddress

    @field_validator('date', mode='before')
    @classmethod
    def format_date_of_taking(cls, value) -> str:
        if value and isinstance(value, datetime):
            return value.isoformat(sep=' ', timespec='seconds')


class PaymentLink(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    url: str
    amount: float


class PositionModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    product_id: int
    count: int


class AttributeModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    key: str
    value: str
    product_id: int


class ProductModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    place_id: int
    description: str
    images: list[str]
    name: str
    price: Decimal
    attributes: list[AttributeModel]

class OrderIdIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
