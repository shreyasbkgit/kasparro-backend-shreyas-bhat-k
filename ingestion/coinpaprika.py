import requests
import json
from datetime import datetime

from core.database import SessionLocal
from core.models import RawCoinPaprika
from core.checkpoints import IngestionCheckpoint

BASE_URL = "https://api.coinpaprika.com/v1/global"

def ingest_coinpaprika():
    response = requests.get(BASE_URL, timeout=10)
    response.raise_for_status()

    data = response.json()
    db = SessionLocal()

    # Store raw payload
    db.add(
        RawCoinPaprika(
            payload=json.dumps(data)
        )
    )

    # Update checkpoint
    checkpoint = (
        db.query(IngestionCheckpoint)
        .filter_by(source="coinpaprika")
        .first()
    )

    if checkpoint:
        checkpoint.last_ingested_at = datetime.utcnow()
    else:
        db.add(
            IngestionCheckpoint(
                source="coinpaprika",
                last_ingested_at=datetime.utcnow()
            )
        )

    db.commit()
    db.close()

