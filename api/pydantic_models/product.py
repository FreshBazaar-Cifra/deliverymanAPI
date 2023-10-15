from pydantic import BaseModel, ConfigDict

class DeliveryProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    images: list[str]
    name: str
    price: int
    weight: int