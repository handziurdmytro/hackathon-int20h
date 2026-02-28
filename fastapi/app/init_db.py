from pathlib import Path
from db import get_conn

DDL_PATH = Path(__file__).with_name("ddl.sql")

def init_db():
    ddl = DDL_PATH.read_text(encoding="utf-8")
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(ddl)
        conn.commit()