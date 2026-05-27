"""Модель платежа за аренду"""
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, Numeric
from app.models import BaseModel, TIMESTAMP, datetime, Decimal, Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.contract import Contract


class Payment(BaseModel):
    """Платёж за аренду"""
    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    contract_id: Mapped[int] = mapped_column(ForeignKey('contracts.id'), index=True, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    due_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    paid_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)

    contract: Mapped['Contract'] = relationship('Contract', back_populates='payments')
