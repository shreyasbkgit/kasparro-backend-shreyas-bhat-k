from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text,
    func,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    name = Column(String)
    price_usd = Column(Float)
    market_cap = Column(Float)
    source = Column(String, index=True)
    ingested_at = Column(DateTime, index=True)


class ETLRun(Base):
    __tablename__ = "etl_runs"

    id = Column(Integer, primary_key=True)
    source = Column(String, index=True)
    status = Column(String)  # success / failure
    records_processed = Column(Integer, default=0)
    duration_ms = Column(Integer)
    started_at = Column(DateTime, server_default=func.now())
    finished_at = Column(DateTime)
    error_message = Column(Text)

