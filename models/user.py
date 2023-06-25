from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


class User(BaseModel):
    id: str = Field(default_factory=ObjectId, alias='_id')
    name: str
    email: str
    password: str
    device_id: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
