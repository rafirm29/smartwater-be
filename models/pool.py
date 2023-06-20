from enum import Enum
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List


class StatusEnum(str, Enum):
    NORMAL = "normal"
    WARNING = "warning"
    DANGER = "danger"


class Pool(BaseModel):
    id: str = Field(default_factory=ObjectId, alias='_id')
    user_email: str
    name: str
    status: StatusEnum = Field(default=StatusEnum.NORMAL)
    anomaly: int = 0
    sensor: List[str] = []

    class Config:
        arbitrary_types_allowed = True
