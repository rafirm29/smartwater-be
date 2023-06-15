from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List


class Pool(BaseModel):
    id: str = Field(default_factory=ObjectId, alias='_id')
    user_email: str
    name: str
    sensor: List[str] = []

    class Config:
        arbitrary_types_allowed = True
