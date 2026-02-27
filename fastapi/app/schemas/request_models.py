# Models for https requests, how they are supposed to look
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class Order(BaseModel):
    id: int = Field(gt=0, description="Unique order ID")
    longitude: float = Field(ge=-180.0, le=180.0)
    latitude: float = Field(ge=-90.0, le=90.0)
    subtotal: float = Field(gt=0.0)
    timestamp: str

    @field_validator('timestamp')
    @classmethod
    def validate_timestamp(cls, v):
        try:
            datetime.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError('timestamp must be in ISO format (e.g., 2023-10-01T12:00:00)')


class TaxRequest(BaseModel):
    longitude: float
    latitude: float
    subtotal: float