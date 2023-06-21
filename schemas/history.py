from pydantic import BaseModel
from typing import Optional, List

from models.history import DataPoint


class HistoryData(BaseModel):
    pool_id: str
    data: List[DataPoint] = []


class SensorData(BaseModel):
    temperature: Optional[float] = None
    ph: Optional[float] = None
