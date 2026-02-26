from schemas import CsvFileWithOrders
from csv_util import stream_csv
from Services.process_order_service import process_order

async def import_csv(csv_order : CsvFileWithOrders):
    async for order in stream_csv(csv_order.csv_file, csv_order.encoding):
        process_order(order)