"""Pydantic схемы для заявок на обслуживание."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.contract import OwnerInfo
from app.schemas.payment import ContractInfo, PropertyInfo, TenantInfo


class RequestCreate(BaseModel):
    """Схема создания заявки."""

    contract_id: int = Field(..., gt=0)
    title: str = Field(..., min_length=3, max_length=255)
    message: str = Field(..., min_length=5, max_length=5000)
    status: str = Field(default="open", min_length=2, max_length=50)


class RequestUpdate(BaseModel):
    """Схема частичного обновления заявки."""

    title: str | None = Field(None, min_length=3, max_length=255)
    message: Optional[str] = Field(default=None, min_length=5, max_length=5000)
    status: Optional[str] = Field(default=None, min_length=2, max_length=50)


class RequestResponse(BaseModel):
    """Схема ответа по заявке."""

    id: int
    contract_id: int
    title: str
    message: str
    status: str

    model_config = ConfigDict(from_attributes=True)


class RequestWithDetailsResponse(RequestResponse):
    """Расширенный ответ с информацией о договоре, объекте и арендаторе."""

    contract_info: ContractInfo | None = None
    property_info: PropertyInfo | None = None
    tenant_info: TenantInfo | None = None  # для владельца
    owner_info: OwnerInfo | None = None  # для арендатора
