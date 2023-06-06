from pydantic import BaseModel


class UserData(BaseModel):
    name: str
    email: str


class UserRegister(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    token: str
