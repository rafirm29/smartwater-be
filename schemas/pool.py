from pydantic import BaseModel
from typing import List


class PoolData(BaseModel):
    id: str
    name: str
    sensor: List[str]


class AddPool(BaseModel):
    name: str
    sensor: List[str]


class AddSensor(BaseModel):
    sensor: List[str]
