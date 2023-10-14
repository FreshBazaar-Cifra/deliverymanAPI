from pydantic import BaseModel, ConfigDict

class Address(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city: str
    district: str | None = None
    street: str
    home: str
    entrance: str | None = None
    apartment: str | None = None