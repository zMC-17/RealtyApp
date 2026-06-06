"""Общие типы SQLAlchemy и базовая модель."""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Date, ForeignKey, Numeric, String, Text, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class BaseModel(Base):
    """Базовая модель со служебными timestamps."""
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

__all__ = [
    "Base",
    "BaseModel",
    "Date",
    "Decimal",
    "ForeignKey",
    "Mapped",
    "Numeric",
    "Optional",
    "String",
    "TIMESTAMP",
    "Text",
    "date",
    "datetime",
    "func",
    "mapped_column",
    "relationship",
]