"""Сервис аутентификации - бизнес-логика"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user import UserCreate, Token


class AuthService:
    """Сервис для работы с аутентификацией и авторизацией"""

    @staticmethod
    async def register_user(
        user_data: UserCreate,
        db: AsyncSession
    ) -> Token:
        """Зарегистрировать нового пользователя + выдать токен"""
        # Проверяем что email уникален
        stmt = select(User).where(User.email == user_data.email)
        result = await db.execute(stmt)
        existing_user = result.scalars().first()

        if existing_user:
            raise ValueError(f"Email {user_data.email} уже зарегистрирован")

        # Хешируем пароль
        hashed_password = hash_password(user_data.password)

        # Создаём пользователя
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=hashed_password
        )

        # Сохраняем в БД
        db.add(new_user)
        await db.flush()  # Чтобы получить ID

        # Создаём access токен
        access_token = create_access_token(
            data={"sub": str(new_user.id)}
        )

        token = Token(
            access_token=access_token
        )

        return token

    @staticmethod
    async def login_user(
        email: str,
        password: str,
        db: AsyncSession
    ) -> Token:
        """Логин пользователя и создание токенов

        Процесс:
        1. Ищем пользователя по email
        2. Проверяем пароль
        3. Создаём access и refresh токены
        4. Возвращаем пользователя и токены

        Args:
            email: Email пользователя
            password: Пароль
            db: Async сессия БД

        Returns:
            Кортеж (пользователь, Token объект)

        Raises:
            ValueError: Если пользователь не найден или пароль неверный
        """
        # Ищем пользователя
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        user = result.scalars().first()

        if not user:
            raise ValueError("Пользователь не найден")

        if not user.password_hash:
            raise ValueError("Пользователь не может войти без пароля")

        # Проверяем пароль
        if not verify_password(password, user.password_hash):
            raise ValueError("Неверный пароль")

        # Создаём access токен (короткоживущий)
        access_token = create_access_token(
            data={"sub": str(user.id)}
        )

        # Возвращаем пользователя и access токен
        token = Token(
            access_token=access_token
        )

        return token
