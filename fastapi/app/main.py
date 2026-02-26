from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from schemas.request_models import Order
from services.orders import process_order, import_csv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/orders")
async def list_orders(name : str = "Dmitriy"):
    #TODO стягувати з бдшок дані
    return {"message": f"Listing orders for {name}:"}

@app.post("/orders")
async def create_order_from_json(order: Order):
    response = await process_order(order)
    return {"message": response.model_dump_json()}

@app.post("/orders/import")
async def import_orders_from_csv(csv_file : UploadFile, encoding: str = "utf-8"):
    #TODO рахувати кількість валідних order і сповіщати користувача про це у відповіді
    await import_csv(csv_file, encoding)

    return {"message": "Orders imported"}
