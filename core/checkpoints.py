from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

BaseCheckpoint = declarative_base()


class IngestionCheckpoint(BaseCheckpoint):
    __tablename__ = "ingestion_checkpoints"

    id = Column(Integer, primary_key=True)
    source = Column(String, unique=True, index=True)
    last_ingested_at = Column(DateTime)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

