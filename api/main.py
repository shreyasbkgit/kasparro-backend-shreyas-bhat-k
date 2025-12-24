from fastapi import FastAPI, Request
import time
import uuid

from sqlalchemy import text

from core.database import engine, SessionLocal
from core.models import Asset
from core.checkpoints import IngestionCheckpoint

app = FastAPI(title="Kasparro Backend API")


@app.get("/health")
def health():
    """
    Health check endpoint.

    Reports:
    - Database connectivity
    - Last ETL run timestamps per source
    """

    db_status = "down"
    etl_status = {}

    # Check database connectivity
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "up"
    except Exception:
        db_status = "down"

    # Fetch ETL last-run status
    db = SessionLocal()
    checkpoints = db.query(IngestionCheckpoint).all()

    for checkpoint in checkpoints:
        etl_status[checkpoint.source] = checkpoint.last_ingested_at

    db.close()

    return {
        "database": db_status,
        "etl_last_run": etl_status
    }


@app.get("/data")
def get_data(
    request: Request,
    limit: int = 10,
    offset: int = 0,
    source: str | None = None,
    symbol: str | None = None
):
    """
    Fetch normalized market observations.

    Supports:
    - Pagination (limit, offset)
    - Filtering by source and symbol

    Returns metadata:
    - request_id
    - api_latency_ms
    """

    start_time = time.time()
    request_id = str(uuid.uuid4())

    db = SessionLocal()
    query = db.query(Asset)

    if source:
        query = query.filter(Asset.source == source)

    if symbol:
        query = query.filter(Asset.symbol == symbol)

    results = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    data = [
        {
            "symbol": row.symbol,
            "name": row.name,
            "price_usd": row.price_usd,
            "market_cap": row.market_cap,
            "source": row.source,
            "ingested_at": row.ingested_at
        }
        for row in results
    ]

    latency_ms = int((time.time() - start_time) * 1000)

    db.close()

    return {
        "request_id": request_id,
        "api_latency_ms": latency_ms,
        "count": len(data),
        "data": data
    }

