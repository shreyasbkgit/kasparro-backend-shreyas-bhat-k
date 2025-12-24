import csv
from datetime import datetime
from pathlib import Path


def load_coingecko_history(csv_path: Path, symbol: str, name: str):
    records = []

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                "symbol": symbol,
                "name": name,
                "price_usd": float(row["price"]),
                "market_cap": float(row["market_cap"]),
                "source": "coingecko_csv",
                "ingested_at": datetime.strptime(
                    row["snapped_at"],
                    "%Y-%m-%d %H:%M:%S UTC"
                )
            })

    return records

