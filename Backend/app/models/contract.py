"""Модель договора аренды"""
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Numeric
from app.models import BaseModel, TIMESTAMP, datetime, Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.property import Properties
    from app.models.user import User
    from app.models.request import Request
    from app.models.payment import Payment


class Contract(BaseModel):
    """Договор аренды между арендодателем и арендатором"""
    __tablename__ = 'contracts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    property_id: Mapped[int] = mapped_column(ForeignKey('properties.id'), index=True, nullable=False)
    tenant_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True, nullable=False)
    start_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    monthly_payment: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    property: Mapped['Properties'] = relationship('Properties', back_populates='contracts')
    tenant: Mapped['User'] = relationship('User', back_populates='contracts')
    requests: Mapped[list['Request']] = relationship('Request', back_populates='contract')
    payments: Mapped[list['Payment']] = relationship('Payment', back_populates='contract')
