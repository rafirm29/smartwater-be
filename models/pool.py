from enum import Enum
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List, Optional


class StatusEnum(str, Enum):
    NORMAL = "normal"
    WARNING = "warning"
    DANGER = "danger"


class SensorType(str, Enum):
    PH = "ph"
    TEMP = "temperature"
    TDS = "tds"


class Anomaly(BaseModel):
    sensor_type: SensorType
    action: str


class Pool(BaseModel):
    id: str = Field(default_factory=ObjectId, alias='_id')
    user_email: str
    name: str
    status: StatusEnum = Field(default=StatusEnum.NORMAL)
    anomaly: Optional[List[Anomaly]] = []
    sensor: List[str] = []

    class Config:
        arbitrary_types_allowed = True
