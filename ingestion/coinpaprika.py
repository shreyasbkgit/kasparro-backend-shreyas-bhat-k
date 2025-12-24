import requests
from datetime import datetime

COINPAPRIKA_GLOBAL_URL = "https://api.coinpaprika.com/v1/global"

def fetch_coinpaprika_global():
    response = requests.get(COINPAPRIKA_GLOBAL_URL, timeout=10)
    response.raise_for_status()
    data = response.json()

    return [{
        "symbol": "MARKET",
        "name": "Global Crypto Market",
        "price_usd": 0.0,  # IMPORTANT: not None
        "market_cap": data.get("market_cap_usd"),
        "source": "coinpaprika",
        "ingested_at": datetime.utcfromtimestamp(data.get("last_updated"))
    }]

    }

