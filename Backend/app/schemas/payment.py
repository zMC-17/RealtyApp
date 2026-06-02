"""Pydantic схемы для платежей."""
from datetime import date, datetime
from decimal import Decimal
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


PaymentStatus = Literal["pending", "waiting_confirmation", "overdue", "paid"]

PAYMENT_STATUS_VALUES: tuple[PaymentStatus, ...] = (
	"pending",
	"waiting_confirmation",
	"overdue",
	"paid",
)


class PaymentCreate(BaseModel):
	"""Схема создания платежа."""
	contract_id: int = Field(..., gt=0)
	amount: Decimal = Field(..., gt=0, max_digits=12, decimal_places=2)
	due_date: date
	status: PaymentStatus = Field(default="pending")
	comment: Optional[str] = Field(default=None, max_length=2000)
	payment_proof_url: Optional[str] = Field(default=None, max_length=2000)
	confirmation_requested_at: Optional[datetime] = None


class PaymentUpdate(BaseModel):
	"""Схема частичного обновления платежа."""
	amount: Optional[Decimal] = Field(default=None, gt=0, max_digits=12, decimal_places=2)
	due_date: Optional[date] = None
	comment: Optional[str] = Field(default=None, max_length=2000)
	payment_proof_url: Optional[str] = Field(default=None, max_length=2000)


class PaymentConfirmationRequest(BaseModel):
	"""Схема запроса подтверждения оплаты от арендатора."""
	payment_proof_url: str = Field(..., min_length=3, max_length=2000)
	comment: Optional[str] = Field(default=None, max_length=2000)


class PaymentResponse(BaseModel):
	"""Схема ответа по платежу."""
	id: int
	contract_id: int
	amount: Decimal
	due_date: date
	paid_at: Optional[datetime]
	status: PaymentStatus
	comment: Optional[str]
	payment_proof_url: Optional[str]
	confirmation_requested_at: Optional[datetime]

	model_config = ConfigDict(from_attributes=True)


class ContractInfo(BaseModel):
	"""Информация о договоре аренды."""
	id: int
	start_date: date
	end_date: date
	monthly_payment: Decimal

	model_config = ConfigDict(from_attributes=True)


class PropertyInfo(BaseModel):
	"""Информация об объекте недвижимости."""
	id: int
	title: str
	address: str

	model_config = ConfigDict(from_attributes=True)


class TenantInfo(BaseModel):
	"""Информация об арендаторе."""
	id: int
	name: str
	email: str

	model_config = ConfigDict(from_attributes=True)


class PaymentWithDetailsResponse(PaymentResponse):
	"""Расширенный ответ по платежу с информацией о договоре, объекте и арендаторе."""
	contract_info: Optional[ContractInfo] = None
	property_info: Optional[PropertyInfo] = None
	tenant_info: Optional[TenantInfo] = None
