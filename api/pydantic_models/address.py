from pydantic import BaseModel, ConfigDict
from pydantic.types import Decimal

class Address(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city: str
    district: str | None = None
    street: str
    home: str
    entrance: str | None = None
    apartment: str | None = None
    latitude: Decimal
    longitude: Decimal

class DeliveryAddress(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    city: str
    district: str | None = None
    street: str
    home: str
    entrance: str | None = None
    apartment: str | None = None
    intercom: str | None = None
    latitude: Decimal
    longitude: Decimal
