from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

BaseCheckpoint = declarative_base()

class IngestionCheckpoint(BaseCheckpoint):
    __tablename__ = "ingestion_checkpoints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source = Column(String, unique=True)
    last_ingested_at = Column(DateTime)

