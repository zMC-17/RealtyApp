"""Управление конфигурацией из переменных окружения"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # БД
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost/dbname"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    # JWT
    SECRET_KEY: str = "ваш-секретный-ключ-минимум-32-символа-используйте-openssl-rand"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


    # Админ
    ADMIN_EMAIL: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()