import json

from fastapi import FastAPI, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    try:
        body = await request.json()
    except:
        body = (await request.body()).decode('utf-8', errors='ignore')
    print(json.dumps(body, indent=2))
    return JSONResponse(status_code=422, content=body)

@app.get("/orders")
async def list_orders():
    #TODO стягувати з бдшок дані
    return list()

@app.post("/orders")
async def create_order_from_json(order: Order):
    response = await process_order(order)
    return {"message": response.model_dump_json()}

@app.post("/orders/import")
async def import_orders_from_csv(csv_file : UploadFile, encoding: str = "utf-8"):
    #TODO рахувати кількість валідних order і сповіщати користувача про це у відповіді
    await import_csv(csv_file, encoding)

    return {"message": "Orders imported"}
