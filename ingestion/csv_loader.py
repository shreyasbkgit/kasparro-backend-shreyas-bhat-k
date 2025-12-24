import csv
import json
from datetime import datetime
from core.database import SessionLocal
from core.models import RawCSVPrices
from core.checkpoints import IngestionCheckpoint

CSV_PATH = "data/coingecko_btc.csv"

def ingest_csv():
    db = SessionLocal()

    checkpoint = (
        db.query(IngestionCheckpoint)
        .filter_by(source="coingecko_csv")
        .first()
    )

    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            db.add(
                RawCSVPrices(
                    payload=json.dumps(row)
                )
            )

    if checkpoint:
        checkpoint.last_ingested_at = datetime.utcnow()
    else:
        db.add(
            IngestionCheckpoint(
                source="coingecko_csv",
                last_ingested_at=datetime.utcnow()
            )
        )

    db.commit()
    db.close()

