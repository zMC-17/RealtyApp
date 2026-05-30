"""Зависимости для FastAPI роутов"""
from typing import AsyncGenerator, Annotated, Optional

from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import async_session_maker
from app.core.security import verify_token
from app.models.user import User


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Зависимость для внедрения сессии БД в роуты.
    Создаёт новую сессию для каждого запроса и закрывает её после.
    """
    async with async_session_maker() as session:
        yield session


async def get_current_user(
    authorization: Annotated[Optional[str], Header()] = None,
    db: AsyncSession = Depends(get_db)
) -> User:
    """Получить текущего пользователя из JWT токена

    Эта зависимость:
    1. Извлекает токен из Authorization заголовка
    2. Валидирует токен
    3. Ищет пользователя в БД
    4. Возвращает пользователя

    Если что-то не так → выбрасывает 401 ошибка

    Использование в роутах:
    @router.get("/me")
    async def get_profile(user: User = Depends(get_current_user)):
        return user
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authorization header required",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Извлекаем токен из "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid scheme")
    except (ValueError, IndexError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Валидируем токен
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный или истёкший токен",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Извлекаем user_id из токена
    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Ищем пользователя в БД
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user
