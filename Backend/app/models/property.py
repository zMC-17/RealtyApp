"""Модель объекта недвижимости"""
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey
from app.models import BaseModel
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.contract import Contract


class Properties(BaseModel):
    """Объект недвижимости - квартира, дом и т.д."""
    __tablename__ = 'properties'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    property_type: Mapped[str] = mapped_column(String(50), nullable=False)

    owner: Mapped['User'] = relationship('User', back_populates='properties')
    contracts: Mapped[list['Contract']] = relationship('Contract', back_populates='property')
