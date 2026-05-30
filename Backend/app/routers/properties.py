"""Роутер для управления объектами недвижимости."""
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.property import PropertyCreate, PropertyResponse, PropertyUpdate
from app.services.property_service import PropertyService


router = APIRouter(prefix="/properties", tags=["properties"])


@router.get("/me", response_model=list[PropertyResponse])
async def list_my_properties(
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> list[PropertyResponse]:
	"""Список объектов текущего владельца."""
	props = await PropertyService.list_owned(current_user.id, db)
	return [PropertyResponse.model_validate(item) for item in props]


@router.post("", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
async def create_property(
	payload: PropertyCreate,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> PropertyResponse:
	"""Создать объект недвижимости для текущего пользователя."""
	property_obj = await PropertyService.create(current_user.id, payload, db)
	return PropertyResponse.model_validate(property_obj)


@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(
	property_id: int,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> PropertyResponse:
	"""Получить один объект, если он принадлежит текущему пользователю."""
	property_obj = await PropertyService.get_if_owned(property_id, current_user.id, db)
	return PropertyResponse.model_validate(property_obj)


@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property(
	property_id: int,
	payload: PropertyUpdate,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> PropertyResponse:
	"""Обновить объект недвижимости."""
	property_obj = await PropertyService.update(property_id, current_user.id, payload, db)
	return PropertyResponse.model_validate(property_obj)


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(
	property_id: int,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> Response:
	"""Удалить объект недвижимости."""
	await PropertyService.delete(property_id, current_user.id, db)
	return Response(status_code=status.HTTP_204_NO_CONTENT)
