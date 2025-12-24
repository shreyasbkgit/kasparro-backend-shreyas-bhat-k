from fastapi import FastAPI, Request
import time
import uuid
from sqlalchemy import text, desc
from core.database import engine, SessionLocal
from core.models import Base, Asset, ETLRun
from core.checkpoints import BaseCheckpoint, IngestionCheckpoint

app = FastAPI(title="Kasparro Backend API")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    BaseCheckpoint.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    db_status = "down"
    etl_status = {}

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "up"
    except Exception:
        db_status = "down"

    db = SessionLocal()
    checkpoints = db.query(IngestionCheckpoint).all()
    for checkpoint in checkpoints:
        etl_status[checkpoint.source] = (
            checkpoint.last_ingested_at.isoformat()
            if checkpoint.last_ingested_at else None
        )
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
    start_time = time.time()
    request_id = str(uuid.uuid4())

    db = SessionLocal()
    query = db.query(Asset)

    if source:
        query = query.filter(Asset.source == source)

    if symbol:
        query = query.filter(Asset.symbol == symbol)

    rows = query.offset(offset).limit(limit).all()

    data = [
        {
            "symbol": r.symbol,
            "name": r.name,
            "price_usd": r.price_usd,
            "market_cap": r.market_cap,
            "source": r.source,
            "ingested_at": r.ingested_at.isoformat() if r.ingested_at else None
        }
        for r in rows
    ]

    latency_ms = int((time.time() - start_time) * 1000)
    db.close()

    return {
        "request_id": request_id,
        "api_latency_ms": latency_ms,
        "count": len(data),
        "data": data
    }


@app.get("/stats")
def get_stats():
    db = SessionLocal()

    runs = (
        db.query(ETLRun)
        .order_by(desc(ETLRun.started_at))
        .all()
    )

    result = [
        {
            "source": r.source,
            "status": r.status,
            "records_processed": r.records_processed,
            "duration_ms": r.duration_ms,
            "started_at": r.started_at.isoformat() if r.started_at else None,
            "finished_at": r.finished_at.isoformat() if r.finished_at else None,
            "error_message": r.error_message
        }
        for r in runs
    ]

    db.close()

    return {
        "total_runs": len(result),
        "runs": result
    }

