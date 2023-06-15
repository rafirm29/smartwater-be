from pydantic import BaseModel, Field
from bson import ObjectId


class User(BaseModel):
    id: str = Field(default_factory=ObjectId, alias='_id')
    name: str
    email: str
    password: str

    class Config:
        arbitrary_types_allowed = True
