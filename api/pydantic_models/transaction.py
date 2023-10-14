from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator

class TransactionModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: str
    sum: int
    type: str

    @field_validator('date', mode='before')
    @classmethod
    def format_date_of_taking(cls, value) -> str:
        if value and isinstance(value, datetime):
            return value.isoformat(sep=' ', timespec='seconds')