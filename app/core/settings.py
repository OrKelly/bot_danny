import pathlib

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    REDIS_HOST: str
    REDIS_PORT: str

    URL_TO_PARSE: str

    @property
    def REDIS_URL(self):
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'

    class Config:
        env_file = f"{pathlib.Path(__file__).resolve().parent.parent.parent}/.env"


config = Settings()
