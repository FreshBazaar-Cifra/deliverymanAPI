from pydantic import BaseModel, ConfigDict

from pydantic_models.product import DeliveryProduct

class DeliveryPosition(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product: DeliveryProduct
    count: int