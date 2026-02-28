from pydantic import BaseModel

class GeoData(BaseModel):
    state_rate: float
    county_rate: float
    city_rate: float
    special_rates: float

class TaxServiceResponse(BaseModel):
    composite_tax_rate: float
    tax_amount: float
    total_amount: float
    breakdown : GeoData
    jurisdictions: list[str]
