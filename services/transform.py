import json
from datetime import datetime
from core.database import SessionLocal
from core.models import RawCoinPaprika, RawCSVPrices, Asset
from schemas.asset import AssetSchema


def transform_coinpaprika():
    """
    Global market observation.
    """

    db = SessionLocal()
    raws = db.query(RawCoinPaprika).all()

    for row in raws:
        data = json.loads(row.payload)

        asset = AssetSchema(
            symbol="MARKET",
            name="Global Crypto Market",
            price_usd=None,
            market_cap=float(data["market_cap_usd"]),
            source="coinpaprika"
        )

        db.add(
            Asset(
                symbol=asset.symbol,
                name=asset.name,
                price_usd=asset.price_usd,
                market_cap=asset.market_cap,
                source=asset.source
            )
        )

    db.commit()
    db.close()


def transform_csv():
    """
    Bitcoin historical price observations.
    """

    db = SessionLocal()
    raws = db.query(RawCSVPrices).all()

    for row in raws:
        data = json.loads(row.payload)

        asset = AssetSchema(
            symbol="BTC",
            name="Bitcoin",
            price_usd=float(data["price"]),
            market_cap=float(data["market_cap"]),
            source="coingecko_csv"
        )

        db.add(
            Asset(
                symbol=asset.symbol,
                name=asset.name,
                price_usd=asset.price_usd,
                market_cap=asset.market_cap,
                source=asset.source,
                ingested_at=datetime.fromisoformat(
                    data["snapped_at"].replace(" UTC", "")
                )
            )
        )

    db.commit()
    db.close()

