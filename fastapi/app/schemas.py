from fastapi import UploadFile
from pydantic import BaseModel, Field


class Order(BaseModel):
    id: int = Field(gt=0) #TODO валідація унікальності id або ж через щось типу Guid
    latitude: float = Field(ge=-90.0, le=90.0)
    longitude: float = Field(ge=-180.0, le=180.0)
    subtotal: float = Field(gt=0.0)
    timestamp: str #TODO валідація формату дати та часу

class CsvFileWithOrders(BaseModel):
    csv_file: UploadFile
    encoding: str = "utf-8"