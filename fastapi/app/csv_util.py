from fastapi import UploadFile


async def stream_csv(csv_file: UploadFile, encoding: str):
    pass