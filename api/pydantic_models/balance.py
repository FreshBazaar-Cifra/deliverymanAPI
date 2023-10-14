from pydantic import BaseModel, ConfigDict
from pydantic.types import Decimal

class BalanceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sum: Decimal