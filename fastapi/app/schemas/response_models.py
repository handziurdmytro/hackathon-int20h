from pydantic import BaseModel


class TaxServiceResponse(BaseModel):
    composite_tax_rate: float
    tax_amount: float
    total_amount: float