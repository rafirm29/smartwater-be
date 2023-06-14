from pydantic import BaseModel
from typing import List


class PoolData(BaseModel):
    name: str
    sensor: List[str]


class AddPool(BaseModel):
    user_email: str
    name: str
    sensor: List[str]
