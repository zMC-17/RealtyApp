# tests/test_basic.py
# python -m pytest tests/test_basic.py -v

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_health_check():
    """Проверка здоровья приложения."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_register_and_login():
    """Полный цикл: регистрация → логин → профиль."""
    import uuid

    unique_id = uuid.uuid4().hex[:8]

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Регистрация
        register_response = await client.post(
            "/auth/register",
            json={
                "name": "Тестовый Пользователь",
                "email": f"test_{unique_id}@example.com",
                "password": "testpassword123",
            },
        )
        assert register_response.status_code == 201
        token_data = register_response.json()
        assert "access_token" in token_data

        # 2. Получаем профиль с токеном
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        profile_response = await client.get("/auth/me", headers=headers)
        assert profile_response.status_code == 200
        profile = profile_response.json()
        assert profile["email"] == f"test_{unique_id}@example.com"
        assert profile["name"] == "Тестовый Пользователь"

        # 3. Логин
        login_response = await client.post(
            "/auth/login",
            json={
                "email": f"test_{unique_id}@example.com",
                "password": "testpassword123",
            },
        )
        assert login_response.status_code == 200

        # 4. Неверный пароль
        bad_login = await client.post(
            "/auth/login",
            json={
                "email": f"test_{unique_id}@example.com",
                "password": "wrongpassword",
            },
        )
        assert bad_login.status_code == 401


@pytest.mark.asyncio
async def test_unauthorized_access():
    """Проверка защиты маршрутов."""
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Без токена — 401
        response = await client.get("/auth/me")
        assert response.status_code == 401

        response = await client.get("/properties/me")
        assert response.status_code == 401

        response = await client.get("/contracts/me")
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_validation_errors():
    """Проверка валидации входных данных."""
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Короткий пароль
        response = await client.post(
            "/auth/register",
            json={
                "name": "Test",
                "email": "test@example.com",
                "password": "123",  # меньше 8 символов
            },
        )
        assert response.status_code == 422

        # Без имени
        response = await client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "testpassword123",
            },
        )
        assert response.status_code == 422
