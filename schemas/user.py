
from pydantic import BaseModel, Field
from bson import ObjectId


class UserData(BaseModel):
    id: str
    name: str
    email: str


class UserRegister(BaseModel):
    name: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)


class UserLogin(BaseModel):
    email: str
    password: str
    device_id: str


class LoginResponse(BaseModel):
    token: str
    name: str
    email: str


class UserChangeName(BaseModel):
    name: str
