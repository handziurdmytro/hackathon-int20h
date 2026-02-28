import json
import os
from fastapi import FastAPI, UploadFile, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from db import get_conn
from init_db import init_db
from schemas.request_models import OrderCreate
from services.orders import process_order, import_csv

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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
async def list_orders(limit: int = 50):
    sql = """
        SELECT id, latitude, longitude, subtotal, order_timestamp,
               jurisdictions
        FROM orders
        LIMIT %s;
    """
    # ORDER BY order_timestamp DESC

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (limit,))
            rows = cur.fetchall()

    return [
        {
            "id": r[0],
            "latitude": r[1],
            "longitude": r[2],
            "subtotal": float(r[3]),
            "order_timestamp": r[4].isoformat(),
            "jurisdictions": r[5] or []
        }
        for r in rows
    ]


@app.post("/orders")
async def create_order_from_json(order: OrderCreate):
    response = await process_order(order)

    sql = """
          INSERT INTO orders (latitude, longitude, subtotal, order_timestamp, \
                              composite_tax_rate, tax_amount, total_amount, \
                              state_rate, county_rate, city_rate, special_rates, \
                              jurisdictions)
          VALUES (%(latitude)s, %(longitude)s, %(subtotal)s, %(order_timestamp)s, \
                  %(composite_tax_rate)s, %(tax_amount)s, %(total_amount)s, \
                  %(state_rate)s, %(county_rate)s, %(city_rate)s, %(special_rates)s, \
                  %(jurisdictions)s::jsonb) RETURNING id; \
          """

    data = response.model_dump()
    breakdown = data.get('breakdown', {})
    db_data = {
        'latitude': data['latitude'],
        'longitude': data['longitude'],
        'subtotal': data['subtotal'],
        'order_timestamp': data['order_timestamp'],
        'composite_tax_rate': data['composite_tax_rate'],
        'tax_amount': data['tax_amount'],
        'total_amount': data['total_amount'],
        'state_rate': breakdown.get('state'),
        'county_rate': breakdown.get('county'),
        'city_rate': breakdown.get('city'),
        'special_rates': breakdown.get('special'),
        'jurisdictions': data.get('jurisdictions', [])
    }

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, db_data)
            new_id = cur.fetchone()[0]
        conn.commit()

    data["id"] = new_id
    return data

@app.post("/orders/import")
async def import_orders_from_csv(csv_file: UploadFile, encoding: str = "utf-8"):
    responses = await import_csv(csv_file, encoding)
    valid_orders = []
    sql = """
          INSERT INTO orders (latitude, longitude, subtotal, order_timestamp, \
                              composite_tax_rate, tax_amount, total_amount, \
                              state_rate, county_rate, city_rate, special_rates, \
                              jurisdictions)
          VALUES (%(latitude)s, %(longitude)s, %(subtotal)s, %(order_timestamp)s, \
                  %(composite_tax_rate)s, %(tax_amount)s, %(total_amount)s, \
                  %(state_rate)s, %(county_rate)s, %(city_rate)s, %(special_rates)s, \
                  %(jurisdictions)s::jsonb) RETURNING id; \
          """
    with get_conn() as conn:
        with conn.cursor() as cur:
            for response in responses:
                if response is not None:  # Assuming None for invalid orders
                    data = response.model_dump()
                    breakdown = data.get('breakdown', {})
                    db_data = {
                        'latitude': data['latitude'],
                        'longitude': data['longitude'],
                        'subtotal': data['subtotal'],
                        'order_timestamp': data['order_timestamp'],
                        'composite_tax_rate': data['composite_tax_rate'],
                        'tax_amount': data['tax_amount'],
                        'total_amount': data['total_amount'],
                        'state_rate': breakdown.get('state'),
                        'county_rate': breakdown.get('county'),
                        'city_rate': breakdown.get('city'),
                        'special_rates': breakdown.get('special'),
                        'jurisdictions': data.get('jurisdictions', [])
                    }
                    cur.execute(sql, db_data)
                    new_id = cur.fetchone()[0]
                    data["id"] = new_id
                    valid_orders.append(data)
        conn.commit()
    return {"orders": valid_orders, "valid_orders_count": len(valid_orders)}

@app.get("/")
async def get_page():
    html_file_path = os.path.join("static", "index.html")
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    return HTMLResponse(content=html_content)
