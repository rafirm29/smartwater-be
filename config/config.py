from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    PATH_TO_PRIVATE_KEY: str
    MONGODB_ADMIN: str
    MONGODB_PASSWORD: str

    class Config:
        env_file = ".env"


settings = Settings()
