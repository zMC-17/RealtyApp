"""Роутер для управления объектами недвижимости."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.property import Property
from app.models.user import User
from app.schemas.property import PropertyCreate, PropertyResponse, PropertyUpdate


router = APIRouter(prefix="/properties", tags=["properties"])


async def _get_owned_property(
	property_id: int,
	current_user: User,
	db: AsyncSession,
) -> Property:
	"""Получить объект и проверить, что он принадлежит текущему пользователю."""
	result = await db.execute(select(Property).where(Property.id == property_id))
	property_obj = result.scalars().first()

	if property_obj is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объект не найден")

	if property_obj.owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа к этому объекту")

	return property_obj


@router.get("/me", response_model=list[PropertyResponse])
async def list_my_properties(
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> list[PropertyResponse]:
	"""Список объектов текущего владельца."""
	result = await db.execute(
		select(Property)
		.where(Property.owner_id == current_user.id)
		.order_by(Property.created_at.desc())
	)
	properties = result.scalars().all()
	return [PropertyResponse.model_validate(item) for item in properties]


@router.post("", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
async def create_property(
	payload: PropertyCreate,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> PropertyResponse:
	"""Создать объект недвижимости для текущего пользователя."""
	property_obj = Property(
		owner_id=current_user.id,
		title=payload.title,
		address=payload.address,
		description=payload.description,
		property_type=payload.property_type,
	)

	db.add(property_obj)
	await db.commit()
	await db.refresh(property_obj)

	return PropertyResponse.model_validate(property_obj)


@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(
	property_id: int,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> PropertyResponse:
	"""Получить один объект, если он принадлежит текущему пользователю."""
	property_obj = await _get_owned_property(property_id, current_user, db)
	return PropertyResponse.model_validate(property_obj)


@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property(
	property_id: int,
	payload: PropertyUpdate,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> PropertyResponse:
	"""Обновить объект недвижимости."""
	property_obj = await _get_owned_property(property_id, current_user, db)

	updates = payload.model_dump(exclude_unset=True)
	for field, value in updates.items():
		setattr(property_obj, field, value)

	await db.commit()
	await db.refresh(property_obj)
	return PropertyResponse.model_validate(property_obj)


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(
	property_id: int,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> Response:
	"""Удалить объект недвижимости."""
	property_obj = await _get_owned_property(property_id, current_user, db)
	await db.delete(property_obj)
	await db.commit()
	return Response(status_code=status.HTTP_204_NO_CONTENT)
