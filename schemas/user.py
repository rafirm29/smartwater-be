from pydantic import BaseModel, Field


class UserData(BaseModel):
    name: str
    email: str


class UserRegister(BaseModel):
    name: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)


class UserLogin(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    token: str
    name: str
    email: str
