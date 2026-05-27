"""Модель заявки на обслуживание"""
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey
from app.models import BaseModel, TIMESTAMP, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.contract import Contract
    from app.models.property import Properties


class Request(BaseModel):
    """Заявка на обслуживание/ремонт от арендатора"""
    __tablename__ = 'requests'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    contract_id: Mapped[int] = mapped_column(ForeignKey('contracts.id'), index=True, nullable=False)
    property_id: Mapped[int] = mapped_column(ForeignKey('properties.id'), index=True, nullable=False)
    message: Mapped[str] = mapped_column(Text(), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    request_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)

    contract: Mapped['Contract'] = relationship('Contract', back_populates='requests')
    property: Mapped['Properties'] = relationship('Properties')