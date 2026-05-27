"""Зависимости для FastAPI роутов"""
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_session_maker
from typing import AsyncGenerator


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Зависимость для внедрения сессии БД в роуты.
    Создаёт новую сессию для каждого запроса и закрывает её после.
    """
    async with async_session_maker() as session:
        yield session
