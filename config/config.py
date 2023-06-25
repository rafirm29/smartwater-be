from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    FCM_SERVER_TOKEN: str

    class Config:
        env_file = ".env"


settings = Settings()
