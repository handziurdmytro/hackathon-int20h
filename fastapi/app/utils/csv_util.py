import csv
import io

from fastapi import UploadFile

def stream_csv(csv_order: UploadFile, encoding: str = "utf-8"):
    text_stream = io.TextIOWrapper(csv_order.file, encoding=encoding)

    reader = csv.DictReader(text_stream)

    for row in reader:
        yield row