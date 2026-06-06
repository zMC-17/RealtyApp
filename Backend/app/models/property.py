"""Модель объекта недвижимости"""
from app.models.base import BaseModel, ForeignKey, Mapped, Optional, String, Text, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.contract import Contract
    from app.models.user import User


class Property(BaseModel):
    """Объект недвижимости - квартира, дом и т.д."""
    __tablename__ = 'properties'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    property_type: Mapped[str] = mapped_column(String(50), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    owner: Mapped['User'] = relationship('User', back_populates='properties')
    contracts: Mapped[list['Contract']] = relationship('Contract', back_populates='property')
