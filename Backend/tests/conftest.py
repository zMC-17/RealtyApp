"""Фикстуры для тестов."""

import asyncio
from typing import AsyncGenerator, List

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.main import app
from app.core.dependencies import get_db
from app.core.database import Base
from app.models.user import User
from app.models.property import Property
from app.models.contract import Contract
from app.models.request import Request
from app.models.payment import Payment
from app.core.security import create_access_token

# Тестовая БД (SQLite in-memory)
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Создаёт чистую БД для каждого теста."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Клиент с подменённой БД."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


# ===== Хелперы для создания тестовых данных =====


def create_test_token(user_id: int = 1, email: str = "test@example.com") -> str:
    """Создать JWT токен для тестов."""
    return create_access_token(data={"sub": email, "user_id": user_id})


def auth_header(token: str = None) -> dict:
    """Заголовок авторизации."""
    if token is None:
        token = create_test_token()
    return {"Authorization": f"Bearer {token}"}


async def create_test_user(db: AsyncSession, **kwargs) -> User:
    """Создать тестового пользователя."""
    defaults = {
        "name": "Test User",
        "email": "test@example.com",
        "password_hash": "$2b$12$LJ3m4ys3GZfnYMz8kVsKaOTSxGHLfEhCgQv7LJpYhWkRcQkFqGjXO",  # "password123"
    }
    defaults.update(kwargs)
    user = User(**defaults)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def create_test_property(db: AsyncSession, owner_id: int, **kwargs) -> Property:
    """Создать тестовый объект недвижимости."""
    defaults = {
        "owner_id": owner_id,
        "title": "Test Property",
        "address": "Test Address 123",
        "property_type": "apartment",
    }
    defaults.update(kwargs)
    prop = Property(**defaults)
    db.add(prop)
    await db.commit()
    await db.refresh(prop)
    return prop


async def create_test_contract(
    db: AsyncSession, property_id: int, tenant_id: int, **kwargs
) -> Contract:
    """Создать тестовый договор."""
    from datetime import date, timedelta

    defaults = {
        "property_id": property_id,
        "tenant_id": tenant_id,
        "start_date": date.today(),
        "end_date": date.today() + timedelta(days=365),
        "monthly_payment": 50000,
        "security_deposit": 50000,
        "status": "active",
    }
    defaults.update(kwargs)
    contract = Contract(**defaults)
    db.add(contract)
    await db.commit()
    await db.refresh(contract)
    return contract