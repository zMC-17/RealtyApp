"""Модели данных приложения"""
from sqlalchemy import String, Text, ForeignKey, TIMESTAMP, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from datetime import datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.contract import Contract
    from app.models.property import Properties
    from app.models.request import Request
    from app.models.payment import Payment


class BaseModel(Base):
    """Абстрактная базовая модель со служебными полями"""
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default='now()'
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default='now()',
        onupdate='now()'
    )


__all__ = [
    'Base',
    'BaseModel',
    'Mapped',
    'mapped_column',
    'relationship',
    'String',
    'Text',
    'Numeric',
    'ForeignKey',
    'TIMESTAMP',
    'datetime',
    'Decimal',
    'Optional',
]