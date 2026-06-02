"""Модель пользователя (арендодатель/арендатор)"""
from typing import TYPE_CHECKING, Optional

from app.models.base import BaseModel, Mapped, String, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.contract import Contract
    from app.models.property import Property


class User(BaseModel):
    """Пользователь системы - может быть арендодателем или арендатором"""
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    password_hash: Mapped[Optional[str]] = mapped_column(nullable=True)

    properties: Mapped[list['Property']] = relationship('Property', back_populates='owner')
    contracts: Mapped[list['Contract']] = relationship('Contract', back_populates='tenant')