from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.types import Decimal

class TransactionModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: str
    sum: Decimal
    type: str

    @field_validator('date', mode='before')
    @classmethod
    def format_date_of_taking(cls, value) -> str:
        if value and isinstance(value, datetime):
            return value.isoformat(sep=' ', timespec='seconds')