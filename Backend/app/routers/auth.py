"""Роутер аутентификации"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserResponse:
    """Регистрация нового пользователя

    Процесс:
    1. Принимаем email, имя и пароль
    2. Валидируем пароль минимум 8 символов
    3. Проверяем что email уникален
    4. Хешируем пароль
    5. Сохраняем в БД
    6. Возвращаем пользователя (без пароля!)
    """
    try:
        new_user = await AuthService.register_user(user_data, db)
        await db.commit()
        return UserResponse.model_validate(new_user)
    except ValueError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> Token:
    """Логин пользователя и получение JWT токенов

     Процесс:
     1. Принимаем email и пароль
     2. Ищем пользователя в БД
     3. Проверяем пароль с помощью bcrypt
     4. Если всё OK, создаём access_token и возвращаем его

     Клиент сохраняет access_token и отправляет его в каждом запросе.
    """
    try:
        user, token = await AuthService.login_user(
            credentials.email,
            credentials.password,
            db
        )
        await db.commit()
        return token
    except ValueError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )





@router.get("/me", response_model=UserResponse)
async def get_profile(
    current_user: Annotated[User, Depends(get_current_user)]
) -> UserResponse:
    """Получить профиль текущего пользователя (защищённый роут)

    Пример защищённого роута:
    - Требует валидный access_token в Authorization заголовке
    - Если токен невалиден или истёк → 401 ошибка
    - Если токен OK → возвращаем пользователя

    Использование клиентом:
    curl -H "Authorization: Bearer <access_token>" http://localhost:8000/auth/me
    """
    return UserResponse.model_validate(current_user)
