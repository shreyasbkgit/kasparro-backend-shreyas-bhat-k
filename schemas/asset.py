from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class AssetSchema(BaseModel):
    symbol: str
    name: str
    price_usd: Optional[float]
    market_cap: Optional[float]
    source: str
    ingested_at: datetime

    class Config:
        from_attributes = True

