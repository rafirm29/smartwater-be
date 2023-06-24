from pydantic import BaseModel
from typing import List, Optional
import datetime


class DataPoint(BaseModel):
    timestamp: datetime.datetime = datetime.datetime.now()
    temperature: Optional[float] = None
    ph: Optional[float] = None
    tds: Optional[float] = None


class History(BaseModel):
    pool_id: str
    data: List[DataPoint] = []
