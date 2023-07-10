from pydantic import BaseModel
from typing import List, Optional
import datetime


class DataPoint(BaseModel):
    timestamp: datetime.datetime = datetime.datetime.now()
    temperature: Optional[float] = None
    do: Optional[float] = None
    turbidity: Optional[float] = None
    ph: Optional[float] = None
    temperature_air: Optional[float] = None
    humidity: Optional[float] = None
    volt_battery: Optional[float] = None
    volt_solar: Optional[float] = None
    tds: Optional[float] = None


class History(BaseModel):
    pool_id: str
    data: List[DataPoint] = []
