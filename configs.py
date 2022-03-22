from pydantic import BaseSettings
from functools import lru_cache
from pathlib import Path

IMAGES_DIR = f'{Path(__file__).resolve().parent.joinpath("images")}'


class Settings(BaseSettings):
    # database
    database_url: str
    postgres_user: str
    postgres_password: str
    postgres_server: str
    postgres_port: int
    postgres_database_name: str
    # jwt
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    image_host: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings() -> Settings:
    return Settings()
