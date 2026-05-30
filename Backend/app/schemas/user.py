"""Pydantic схемы для User."""
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Схема для регистрации пользователя"""
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Иван Петров",
                "email": "ivan@example.com",
                "password": "securepass123"
            }
        }


class UserLogin(BaseModel):
    """Схема для логина"""
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "ivan@example.com",
                "password": "securepass123"
            }
        }


class UserResponse(BaseModel):
    """Схема для ответа пользователя (без пароля!)"""
    id: int
    name: str
    email: str
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """Схема частичного обновления пользователя."""
    name: Optional[str] = Field(default=None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8)


class Token(BaseModel):
    """Схема для JWT токена в ответе"""
    access_token: str
    token_type: str = "bearer"

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class TokenData(BaseModel):
    """Данные из JWT токена"""
    user_id: Optional[int] = None
