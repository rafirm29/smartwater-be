from pydantic import BaseModel
from typing import List


class PoolData(BaseModel):
    name: str
    sensor: List[str]


class AddPool(BaseModel):
    name: str
    sensor: List[str]
