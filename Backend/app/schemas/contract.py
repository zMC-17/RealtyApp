"""Pydantic схемы для договора аренды."""
from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ContractCreate(BaseModel):
	"""Схема создания договора аренды."""
	property_id: int = Field(..., gt=0)
	tenant_id: int = Field(..., gt=0)
	start_date: date
	end_date: date
	monthly_payment: Decimal = Field(..., gt=0, max_digits=12, decimal_places=2)
	security_deposit: Decimal = Field(default=Decimal("0"), ge=0, max_digits=12, decimal_places=2)
	status: str = Field(default="active", min_length=2, max_length=50)

	@model_validator(mode="after")
	def validate_dates(self) -> "ContractCreate":
		if self.end_date <= self.start_date:
			raise ValueError("Дата окончания должна быть позже даты начала")
		return self


class ContractCreateByEmail(BaseModel):
	"""Схема создания договора аренды по email арендатора."""
	property_id: int = Field(..., gt=0)
	tenant_email: str = Field(..., min_length=5, max_length=255)
	start_date: date
	end_date: date
	monthly_payment: Decimal = Field(..., gt=0, max_digits=12, decimal_places=2)
	security_deposit: Decimal = Field(default=Decimal("0"), ge=0, max_digits=12, decimal_places=2)
	status: str = Field(default="pending_tenant_confirmation", min_length=2, max_length=50)

	@model_validator(mode="after")
	def validate_dates(self) -> "ContractCreateByEmail":
		if self.end_date <= self.start_date:
			raise ValueError("Дата окончания должна быть позже даты начала")
		return self


class ContractUpdate(BaseModel):
	"""Схема частичного обновления договора аренды."""
	start_date: Optional[date] = None
	end_date: Optional[date] = None
	monthly_payment: Optional[Decimal] = Field(default=None, gt=0, max_digits=12, decimal_places=2)
	security_deposit: Optional[Decimal] = Field(default=None, ge=0, max_digits=12, decimal_places=2)
	status: Optional[str] = Field(default=None, min_length=2, max_length=50)

	@model_validator(mode="after")
	def validate_dates(self) -> "ContractUpdate":
		if self.start_date and self.end_date and self.end_date <= self.start_date:
			raise ValueError("Дата окончания должна быть позже даты начала")
		return self


class ContractResponse(BaseModel):
	"""Схема ответа по договору аренды."""
	id: int
	property_id: int
	tenant_id: int
	start_date: date
	end_date: date
	monthly_payment: Decimal
	security_deposit: Decimal
	status: str

	model_config = ConfigDict(from_attributes=True)
