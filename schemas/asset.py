from pydantic import BaseModel, Field

class AssetSchema(BaseModel):
    symbol: str = Field(..., min_length=1)
    name: str
    price_usd: float | None = None
    market_cap: float | None = None
    source: str

