# Models for https requests, how they are supposed to look
from typing import Optional

from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class TaxBreakdown(BaseModel):
    state_rate: float
    county_rate: float
    city_rate: float
    special_rates: float
    jurisdictions: list[str]


class Order(BaseModel):
    id: Optional[int] = None
    longitude: float = Field(ge=-180.0, le=180.0)
    latitude: float = Field(ge=-90.0, le=90.0)
    subtotal: float = Field(gt=0.0)
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    composite_tax_rate: Optional[float] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None
    breakdown: Optional[TaxBreakdown] = None

    @field_validator('timestamp')
    @classmethod
    def validate_timestamp(cls, v):
        try:
            datetime.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError('timestamp must be in ISO format (e.g., 2023-10-01T12:00:00)')


class TaxRequest(BaseModel):
    latitude: float
    longitude: float
    subtotal: float