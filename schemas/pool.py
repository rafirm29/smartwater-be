from pydantic import BaseModel
from typing import List

from models.pool import StatusEnum, Anomaly


class PoolData(BaseModel):
    id: str
    name: str
    status: StatusEnum
    anomaly: List[Anomaly]
    sensor: List[str]


class AddPool(BaseModel):
    name: str
    sensor: List[str]


class AddSensor(BaseModel):
    sensor: List[str]


class UpdatePoolName(BaseModel):
    name: str
