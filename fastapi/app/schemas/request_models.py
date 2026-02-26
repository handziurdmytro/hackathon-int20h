# Models for https requests, how they are supposed to look
from pydantic import BaseModel, Field


class Order(BaseModel):
    id: int = Field(gt=0) #TODO валідація унікальності id або ж через щось типу Guid
    longitude: float = Field(ge=-180.0, le=180.0)
    latitude: float = Field(ge=-90.0, le=90.0)
    subtotal: float = Field(gt=0.0)
    timestamp: str #TODO валідація формату дати та часу

class TaxRequest(BaseModel):
    longitude: float
    latitude: float
    subtotal: float