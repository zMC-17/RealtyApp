"""Основной модуль FastAPI приложения"""
from fastapi import FastAPI
from app.core.config import settings

# Импорт моделей для регистрации в Base (нужно для миграций Alembic)
from app.models.user import User
from app.models.property import Properties
from app.models.contract import Contract
from app.models.request import Request
from app.models.payment import Payment


app = FastAPI(
    title="Realty Management API",
    description="API для управления недвижимостью и арендой",
    version="1.0.0"
)


@app.get("/health")
async def health_check():
    """Проверка здоровья приложения"""
    return {"status": "ok"}