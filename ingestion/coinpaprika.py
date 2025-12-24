import requests
import json
from core.database import SessionLocal
from core.models import RawCoinPaprika

BASE_URL = "https://api.coinpaprika.com/v1/global"

def ingest_coinpaprika():
    """
    Ingest global crypto market metrics from CoinPaprika.
    Free-tier endpoint, no authentication required.
    """

    response = requests.get(BASE_URL, timeout=10)
    response.raise_for_status()

    data = response.json()
    db = SessionLocal()

    db.add(
        RawCoinPaprika(
            payload=json.dumps(data)
        )
    )

    db.commit()
    db.close()

