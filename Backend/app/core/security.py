"""Функции безопасности: хеширование паролей, JWT токены"""
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

from fastapi.security import HTTPBearer

security = HTTPBearer(auto_error=True, description="JWT токен для аутентификации")  # Схема для извлечения токена из заголовка Authorization

# Контекст для хеширования паролей с bcrypt.
# Примечание: passlib может выдать предупреждение про bcrypt версию,
# но хеширование работает корректно.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Хешировать пароль с помощью bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверить совпадает ли пароль с хешем"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создать JWT access токен

    Args:
        data: Данные для кодирования (например, {"sub": user_id})
        expires_delta: Кастомный срок жизни токена

    Returns:
        Подписанный JWT токен
    """
    to_encode = data.copy()

    # Если не указано, используем дефолтный срок из конфига
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # Добавляем время истечения в payload
    to_encode.update({"exp": expire})

    # Кодируем JWT
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Проверить и декодировать JWT токен

    Args:
        token: JWT токен

    Returns:
        Payload токена если валиден, None если невалиден/истёк
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None
