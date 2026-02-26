from fastapi import UploadFile
from schemas.request_models import Order, TaxRequest
from services.tax_client import TaxServiceClient
from utils.csv_util import stream_csv


async def process_order(order : Order):
    tax_service_request : dict =  {
        "longitude": order.longitude,
        "latitude": order.latitude,
        "subtotal": order.subtotal,
    }

    tax_client = TaxServiceClient(url="http://localhost:3030") #TODO port config file
    response = await tax_client.get_tax_response(TaxRequest(**tax_service_request))
    #TODO зберігати в бдшку дані про замовлення та відповідь від сервісу
    return response


async def import_csv(csv_file: UploadFile, encoding: str = "utf-8"):

    for row in stream_csv(csv_file, encoding):
        order = Order(**row) # перетворює словник на параметри з відповідними назвами
        await process_order(order)
