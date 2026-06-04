"""Тесты авторизации."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Регистрация нового пользователя."""
    response = await client.post(
        "/auth/register",
        json={
            "name": "Иван Петров",
            "email": "ivan@example.com",
            "password": "securepass123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    """Логин существующего пользователя."""
    # Сначала регистрируем
    await client.post(
        "/auth/register",
        json={
            "name": "Иван Петров",
            "email": "ivan@example.com",
            "password": "securepass123",
        },
    )

    # Логинимся
    response = await client.post(
        "/auth/login",
        json={
            "email": "ivan@example.com",
            "password": "securepass123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient):
    """Логин с неверным паролем."""
    await client.post(
        "/auth/register",
        json={
            "name": "Иван Петров",
            "email": "ivan@example.com",
            "password": "securepass123",
        },
    )

    response = await client.post(
        "/auth/login",
        json={
            "email": "ivan@example.com",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_profile_unauthorized(client: AsyncClient):
    """Получение профиля без токена."""
    response = await client.get("/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Проверка здоровья приложения."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
