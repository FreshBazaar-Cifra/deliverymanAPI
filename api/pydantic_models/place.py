from datetime import time

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.types import Decimal
from pydantic_models.address import DeliveryAddress

class DeliveryMarketModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    address: DeliveryAddress
