"""Юнит-тесты для сервиса авторизации."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException

from app.services.auth_service import AuthService
from app.models.user import User


class TestAuthService:
    """Тесты AuthService."""

    @pytest.mark.asyncio
    async def test_register_user_success(self, mocker):
        """Успешная регистрация нового пользователя."""
        mock_db = AsyncMock()

        # Мокаем проверку существования email
        mock_db.execute.return_value.scalars.return_value.first.return_value = None

        # Мокаем flush, commit, refresh
        mock_db.flush = AsyncMock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        user = User(
            name="Test User",
            email="new@example.com",
            password_hash="hashed_password",
        )

        # Мокаем add чтобы вернуть нашего пользователя
        async def mock_refresh(u):
            u.id = 1

        mock_db.refresh = mock_refresh

        result = await AuthService.register_user(
            db=mock_db,
            email="new@example.com",
            name="Test User",
            password="password123",
        )

        assert result.email == "new@example.com"
        assert result.name == "Test User"

    @pytest.mark.asyncio
    async def test_register_existing_email(self, mocker):
        """Регистрация с уже существующим email."""
        mock_db = AsyncMock()

        # Мокаем что пользователь уже есть
        existing_user = User(
            email="exists@example.com", name="Exists", password_hash="hash"
        )
        mock_db.execute.return_value.scalars.return_value.first.return_value = (
            existing_user
        )

        with pytest.raises(HTTPException) as exc:
            await AuthService.register_user(
                db=mock_db,
                email="exists@example.com",
                name="Test",
                password="password123",
            )

        assert exc.value.status_code == 400
        assert "Email уже зарегистрирован" in exc.value.detail

    @pytest.mark.asyncio
    async def test_login_success(self, mocker):
        """Успешный вход с правильным паролем."""
        mock_db = AsyncMock()

        # Создаём пользователя с хешированным паролем
        from passlib.context import CryptContext

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        user = User(
            id=1,
            email="user@example.com",
            name="User",
            password_hash=pwd_context.hash("correct_password"),
        )
        mock_db.execute.return_value.scalars.return_value.first.return_value = user

        # Мокаем создание токена
        mocker.patch(
            "app.services.auth_service.create_access_token",
            return_value="test_token_123",
        )

        result = await AuthService.login_user(
            db=mock_db,
            email="user@example.com",
            password="correct_password",
        )

        assert result["access_token"] == "test_token_123"
        assert result["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, mocker):
        """Вход с неверным паролем."""
        mock_db = AsyncMock()

        from passlib.context import CryptContext

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        user = User(
            email="user@example.com",
            password_hash=pwd_context.hash("correct_password"),
        )
        mock_db.execute.return_value.scalars.return_value.first.return_value = user

        with pytest.raises(HTTPException) as exc:
            await AuthService.login_user(
                db=mock_db,
                email="user@example.com",
                password="wrong_password",
            )

        assert exc.value.status_code == 401

    @pytest.mark.asyncio
    async def test_login_user_not_found(self, mocker):
        """Вход с несуществующим email."""
        mock_db = AsyncMock()
        mock_db.execute.return_value.scalars.return_value.first.return_value = None

        with pytest.raises(HTTPException) as exc:
            await AuthService.login_user(
                db=mock_db,
                email="notfound@example.com",
                password="password123",
            )

        assert exc.value.status_code == 401
