import time
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv("DATABASE_URL")

def wait_for_db(retries=30, delay=2):
    engine = create_engine(DATABASE_URL)

    for i in range(retries):
        try:
            with engine.connect():
                print("Database is ready")
                return
        except OperationalError:
            print(f"Waiting for database... ({i+1}/{retries})")
            time.sleep(delay)

    raise RuntimeError("Database not ready after waiting")
