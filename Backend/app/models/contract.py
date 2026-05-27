"""Модель договора аренды"""
from datetime import date

from app.models.base import BaseModel, Date, Decimal, ForeignKey, Mapped, Numeric, String, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.property import Property
    from app.models.user import User
    from app.models.request import Request
    from app.models.payment import Payment


class Contract(BaseModel):
    """Договор аренды между арендодателем и арендатором"""
    __tablename__ = 'contracts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    property_id: Mapped[int] = mapped_column(ForeignKey('properties.id'), index=True, nullable=False)
    tenant_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True, nullable=False)
    start_date: Mapped[date] = mapped_column(Date(), nullable=False)
    end_date: Mapped[date] = mapped_column(Date(), nullable=False)
    monthly_payment: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    security_deposit: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, server_default="0")
    status: Mapped[str] = mapped_column(String(50), nullable=False)

    property: Mapped['Property'] = relationship('Property', back_populates='contracts')
    tenant: Mapped['User'] = relationship('User', back_populates='contracts')
    requests: Mapped[list['Request']] = relationship('Request', back_populates='contract')
    payments: Mapped[list['Payment']] = relationship('Payment', back_populates='contract')
