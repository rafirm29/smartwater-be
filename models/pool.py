from pydantic import BaseModel
from typing import List


class Pool(BaseModel):
    user_email: str
    name: str
    sensor: List[str] = []
