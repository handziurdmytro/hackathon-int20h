import json
import os

from fastapi import FastAPI, UploadFile, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from schemas.request_models import Order
from services.orders import process_order, import_csv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


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

    return response.model_dump()

@app.post("/orders/import")
async def import_orders_from_csv(csv_file : UploadFile, encoding: str = "utf-8"):
    #TODO рахувати кількість валідних order і сповіщати користувача про це у відповіді
    responses =  await import_csv(csv_file, encoding)

    return {"orders": [r.model_dump() for r in responses]}

@app.get("/")
async def get_page():
    html_file_path = os.path.join("static", "index.html")
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    return HTMLResponse(content=html_content)
