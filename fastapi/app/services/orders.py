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

async def process_orders(orders : list[Order]):
    requests = list()

    for order in orders:
        tax_service_request : dict =  {
            "longitude": order.longitude,
            "latitude": order.latitude,
            "subtotal": order.subtotal,
        }
        requests.append(TaxRequest(**tax_service_request))

    tax_client = TaxServiceClient(url="http://localhost:3030") #TODO port config file
    responses = await tax_client.get_tax_responses(requests)
    #TODO зберігати в бдшку дані про замовлення та відповідь від сервісу
    return responses


async def import_csv(csv_file: UploadFile, encoding: str = "utf-8"):
    orders = list()

    for row in stream_csv(csv_file, encoding):
        order = Order(**row)
        orders.append(order)

        if orders.len > 1000:
            for order in orders:
                await process_orders(order)
            orders.clear()
