from fastapi import FastAPI
from schemas import Order, CsvFileWithOrders
from csv_util import stream_csv
from Services.process_order_service import process_order
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello Dmitriy"}

@app.get("/orders")
async def list_orders(name : str = "Dmitriy"):
    return {"message": f"Listing orders for {name}:"}

@app.post("/orders")
async def create_order_from_json(order: Order):
    process_order(order)

    return {"message": "Order created"}

@app.post("/orders/import")
async def import_orders_from_csv(csv_order : CsvFileWithOrders):
    #TODO рахувати кількість валідних order і сповіщувати користувача про це у відповіді
    async for order in stream_csv(csv_order.csv_file, csv_order.encoding):
        process_order(order)

    return {"message": "Orders imported"}

