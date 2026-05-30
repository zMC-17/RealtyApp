"""Pydantic схемы для заявок на обслуживание."""
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RequestCreate(BaseModel):
	"""Схема создания заявки."""
	contract_id: int = Field(..., gt=0)
	message: str = Field(..., min_length=5, max_length=5000)
	status: str = Field(default="open", min_length=2, max_length=50)


class RequestUpdate(BaseModel):
	"""Схема частичного обновления заявки."""
	message: Optional[str] = Field(default=None, min_length=5, max_length=5000)
	status: Optional[str] = Field(default=None, min_length=2, max_length=50)


class RequestResponse(BaseModel):
	"""Схема ответа по заявке."""
	id: int
	contract_id: int
	message: str
	status: str

	model_config = ConfigDict(from_attributes=True)
