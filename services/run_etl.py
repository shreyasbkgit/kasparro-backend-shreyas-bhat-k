import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import time
import pandas as pd
from datetime import datetime, UTC

from core.database import SessionLocal
from core.init_db import init_db
from core.models import Asset, ETLRun
from core.checkpoints import IngestionCheckpoint

import requests


COINPAPRIKA_GLOBAL_URL = "https://api.coinpaprika.com/v1/global"


def ingest_coingecko(db):
    start = time.time()

    run = ETLRun(
        source="coingecko",
        status="running",
        started_at=datetime.now(UTC)
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    total = 0

    files = [
        ("BTC", "data/coingecko_btc.csv"),
        ("ETH", "data/coingecko_eth.csv")
    ]

    for symbol, path in files:
        df = pd.read_csv(path)

        for _, row in df.iterrows():
            asset = Asset(
                symbol=symbol,
                name=symbol,
                price_usd=row["price"],
                market_cap=row.get("market_cap"),
                source="coingecko",
                ingested_at=datetime.now(UTC)
            )
            db.add(asset)
            total += 1

    checkpoint = db.query(IngestionCheckpoint).filter_by(source="coingecko").first()
    if not checkpoint:
        checkpoint = IngestionCheckpoint(source="coingecko")
        db.add(checkpoint)

    checkpoint.last_ingested_at = datetime.now(UTC)

    run.status = "success"
    run.records_processed = total
    run.finished_at = datetime.now(UTC)
    run.duration_ms = int((time.time() - start) * 1000)

    db.commit()


def ingest_coinpaprika(db):
    start = time.time()

    run = ETLRun(
        source="coinpaprika",
        status="running",
        started_at=datetime.now(UTC)
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    response = requests.get(COINPAPRIKA_GLOBAL_URL, timeout=10)
    response.raise_for_status()
    data = response.json()

    asset = Asset(
        symbol="MARKET",
        name="Global Crypto Market",
        price_usd=None,
        market_cap=data.get("market_cap_usd"),
        source="coinpaprika",
        ingested_at=datetime.now(UTC)
    )

    db.add(asset)

    checkpoint = db.query(IngestionCheckpoint).filter_by(source="coinpaprika").first()
    if not checkpoint:
        checkpoint = IngestionCheckpoint(source="coinpaprika")
        db.add(checkpoint)

    checkpoint.last_ingested_at = datetime.now(UTC)

    run.status = "success"
    run.records_processed = 1
    run.finished_at = datetime.now(UTC)
    run.duration_ms = int((time.time() - start) * 1000)

    db.commit()


def run_etl():
    init_db()
    db = SessionLocal()

    try:
        ingest_coingecko(db)
        ingest_coinpaprika(db)
    finally:
        db.close()


if __name__ == "__main__":
    run_etl()

