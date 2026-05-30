"""Pydantic схемы для объекта недвижимости."""
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PropertyCreate(BaseModel):
	"""Схема создания объекта недвижимости."""
	title: str = Field(..., min_length=3, max_length=255)
	address: str = Field(..., min_length=5, max_length=255)
	description: Optional[str] = Field(default=None, max_length=5000)
	property_type: str = Field(..., min_length=2, max_length=50)


class PropertyUpdate(BaseModel):
	"""Схема частичного обновления объекта недвижимости."""
	title: Optional[str] = Field(default=None, min_length=3, max_length=255)
	address: Optional[str] = Field(default=None, min_length=5, max_length=255)
	description: Optional[str] = Field(default=None, max_length=5000)
	property_type: Optional[str] = Field(default=None, min_length=2, max_length=50)


class PropertyResponse(BaseModel):
	"""Схема ответа по объекту недвижимости."""
	id: int
	owner_id: int
	title: str
	address: str
	description: Optional[str]
	property_type: str

	model_config = ConfigDict(from_attributes=True)
