"""Pydantic схемы для платежей."""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PaymentCreate(BaseModel):
	"""Схема создания платежа."""
	contract_id: int = Field(..., gt=0)
	amount: Decimal = Field(..., gt=0, max_digits=12, decimal_places=2)
	due_date: date
	status: str = Field(default="pending", min_length=2, max_length=50)
	comment: Optional[str] = Field(default=None, max_length=2000)


class PaymentUpdate(BaseModel):
	"""Схема частичного обновления платежа."""
	amount: Optional[Decimal] = Field(default=None, gt=0, max_digits=12, decimal_places=2)
	due_date: Optional[date] = None
	paid_at: Optional[datetime] = None
	status: Optional[str] = Field(default=None, min_length=2, max_length=50)
	comment: Optional[str] = Field(default=None, max_length=2000)


class PaymentResponse(BaseModel):
	"""Схема ответа по платежу."""
	id: int
	contract_id: int
	amount: Decimal
	due_date: date
	paid_at: Optional[datetime]
	status: str
	comment: Optional[str]

	model_config = ConfigDict(from_attributes=True)
