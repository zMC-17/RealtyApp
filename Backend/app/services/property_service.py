"""Сервис для управления объектами недвижимости (CRUD)."""
from typing import Annotated, List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.property import Property
from app.schemas.property import PropertyCreate, PropertyUpdate


class PropertyService:
	@staticmethod
	async def list_owned(owner_id: int, db: AsyncSession) -> List[Property]:
		stmt = select(Property).where(Property.owner_id == owner_id).order_by(Property.created_at.desc())
		result = await db.execute(stmt)
		return result.scalars().all()

	@staticmethod
	async def create(owner_id: int, payload: PropertyCreate, db: AsyncSession) -> Property:
		prop = Property(
			owner_id=owner_id,
			title=payload.title,
			address=payload.address,
			description=payload.description,
			property_type=payload.property_type,
		)
		db.add(prop)
		await db.flush()
		return prop

	@staticmethod
	async def get_if_owned(property_id: int, owner_id: int, db: AsyncSession) -> Property:
		stmt = select(Property).where(Property.id == property_id)
		result = await db.execute(stmt)
		prop = result.scalars().first()

		if prop is None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объект не найден")

		if prop.owner_id != owner_id:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа к этому объекту")

		return prop

	@staticmethod
	async def update(property_id: int, owner_id: int, payload: PropertyUpdate, db: AsyncSession) -> Property:
		prop = await PropertyService.get_if_owned(property_id, owner_id, db)
		updates = payload.model_dump(exclude_unset=True)
		for field, value in updates.items():
			setattr(prop, field, value)
		await db.flush()
		return prop

	@staticmethod
	async def delete(property_id: int, owner_id: int, db: AsyncSession) -> None:
		prop = await PropertyService.get_if_owned(property_id, owner_id, db)
		await db.delete(prop)
