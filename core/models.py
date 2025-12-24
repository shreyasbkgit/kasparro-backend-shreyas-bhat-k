from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class RawCoinPaprika(Base):
    __tablename__ = "raw_coinpaprika"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    payload = Column(String)
    ingested_at = Column(DateTime, default=datetime.utcnow)


class RawCSVPrices(Base):
    __tablename__ = "raw_csv_prices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    payload = Column(String)
    ingested_at = Column(DateTime, default=datetime.utcnow)


class Asset(Base):
    """
    Unified observation table.
    Can represent:
    - Asset-level observations (e.g., BTC)
    - Market-level observations (GLOBAL MARKET)
    """
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String)
    name = Column(String)
    price_usd = Column(Float, nullable=True)
    market_cap = Column(Float, nullable=True)
    source = Column(String)
    ingested_at = Column(DateTime, default=datetime.utcnow)

