from pydantic import BaseModel
from typing import List

from models.pool import StatusEnum


class PoolData(BaseModel):
    id: str
    name: str
    status: StatusEnum
    anomaly: int
    sensor: List[str]


class AddPool(BaseModel):
    name: str
    sensor: List[str]


class AddSensor(BaseModel):
    sensor: List[str]
