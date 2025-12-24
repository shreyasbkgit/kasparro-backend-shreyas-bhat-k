from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime


class HealthSchema(BaseModel):
    database: str
    etl_last_run: Dict[str, Optional[datetime]]

