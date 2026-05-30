"""Основной модуль FastAPI приложения."""
from fastapi import FastAPI
from app.core.config import settings
from app.routers import auth, contracts, payments, properties, requests

# Импорт моделей для регистрации в Base (нужно для миграций Alembic)
from app.models.user import User
from app.models.property import Property
from app.models.contract import Contract
from app.models.request import Request
from app.models.payment import Payment


app = FastAPI(
    title="Realty Management API",
    description="API для управления недвижимостью и арендой",
    version="1.0.0"
)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(properties.router)
app.include_router(contracts.router)
app.include_router(payments.router)
app.include_router(requests.router)

@app.get("/health")
async def health_check():
    """Проверка здоровья приложения"""
    return {"status": "ok"}