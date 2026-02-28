from fastapi import UploadFile
from schemas.request_models import OrderCreate, TaxRequest, TaxBreakdown
from services.tax_client import TaxServiceClient
from utils.csv_util import stream_csv


async def process_order(order : OrderCreate):
    tax_service_request : dict =  {
        "longitude": order.longitude,
        "latitude": order.latitude,
        "subtotal": order.subtotal,
    }

    tax_client = TaxServiceClient(url="http://localhost:3030") #TODO port config file
    response = await tax_client.get_tax_response(TaxRequest(**tax_service_request))
    order.composite_tax_rate = response.composite_tax_rate
    order.tax_amount = response.tax_amount
    order.total_amount = response.total_amount
    order.breakdown = TaxBreakdown(**response.breakdown.model_dump())
    return order

async def process_orders(orders : list[OrderCreate]):
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
    for i, response in enumerate(responses):
        orders[i].composite_tax_rate = response.composite_tax_rate
        orders[i].tax_amount = response.tax_amount
        orders[i].total_amount = response.total_amount
        orders[i].breakdown = TaxBreakdown(**response.breakdown.model_dump())
    #TODO зберігати в бдшку дані про замовлення та відповідь від сервісу
    return orders


async def import_csv(csv_file: UploadFile, encoding: str = "utf-8"):
    orders = list()
    responses = list()

    for row in stream_csv(csv_file, encoding):
        try:
            order = OrderCreate(**row)
            orders.append(order)

            if len(orders) >= 1000:
                batch_responses = await process_orders(orders)
                responses.extend(batch_responses)
                orders.clear()
        except Exception as e:
            print(f"Skipping invalid row: {row}, error: {e}")
            continue

    if orders:
        try:
            batch_responses = await process_orders(orders)
            responses.extend(batch_responses)
        except Exception as e:
            print(f"Error processing batch: {e}")

    return responses
