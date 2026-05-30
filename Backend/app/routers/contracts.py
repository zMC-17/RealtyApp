"""Роутер для договоров аренды."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.contract import Contract
from app.models.property import Property
from app.models.user import User
from app.schemas.contract import ContractCreate, ContractResponse, ContractUpdate


router = APIRouter(prefix="/contracts", tags=["contracts"])


async def _get_contract_with_access(
	contract_id: int,
	current_user: User,
	db: AsyncSession,
) -> Contract:
	"""Получить договор и проверить, что он доступен текущему пользователю."""
	result = await db.execute(
		select(Contract).join(Property).where(Contract.id == contract_id)
	)
	contract_obj = result.scalars().first()

	if contract_obj is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Договор не найден")

	result = await db.execute(select(Property.owner_id).where(Property.id == contract_obj.property_id))
	owner_id = result.scalar_one_or_none()

	if owner_id is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объект по договору не найден")

	if current_user.id not in (contract_obj.tenant_id, owner_id):
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа к этому договору")

	return contract_obj


async def _get_owned_contract(
	contract_id: int,
	current_user: User,
	db: AsyncSession,
) -> Contract:
	"""Получить договор только для владельца объекта."""
	contract_obj = await _get_contract_with_access(contract_id, current_user, db)
	result = await db.execute(select(Property.owner_id).where(Property.id == contract_obj.property_id))
	owner_id = result.scalar_one_or_none()

	if owner_id is None or owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Только владелец может изменять этот договор")

	return contract_obj


@router.get("/me", response_model=list[ContractResponse])
async def list_my_contracts(
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> list[ContractResponse]:
	"""Все договоры, связанные с текущим пользователем."""
	result = await db.execute(
		select(Contract)
		.join(Property)
		.where(or_(Contract.tenant_id == current_user.id, Property.owner_id == current_user.id))
		.order_by(Contract.created_at.desc())
	)
	contracts = list(result.scalars().all())
	return [ContractResponse.model_validate(item) for item in contracts]


@router.get("/owner/me", response_model=list[ContractResponse])
async def list_my_owner_contracts(
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> list[ContractResponse]:
	"""Договоры по объектам текущего владельца."""
	result = await db.execute(
		select(Contract)
		.join(Property)
		.where(Property.owner_id == current_user.id)
		.order_by(Contract.created_at.desc())
	)
	contracts = list(result.scalars().all())
	return [ContractResponse.model_validate(item) for item in contracts]


@router.get("/tenant/me", response_model=list[ContractResponse])
async def list_my_tenant_contracts(
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> list[ContractResponse]:
	"""Договоры текущего арендатора."""
	result = await db.execute(
		select(Contract)
		.where(Contract.tenant_id == current_user.id)
		.order_by(Contract.created_at.desc())
	)
	contracts = list(result.scalars().all())
	return [ContractResponse.model_validate(item) for item in contracts]


@router.post("", response_model=ContractResponse, status_code=status.HTTP_201_CREATED)
async def create_contract(
	payload: ContractCreate,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> ContractResponse:
	"""Создать договор аренды для объекта текущего владельца."""
	property_result = await db.execute(select(Property).where(Property.id == payload.property_id))
	property_obj = property_result.scalars().first()

	if property_obj is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объект не найден")

	if property_obj.owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Создавать договор может только владелец объекта")

	tenant_result = await db.execute(select(User).where(User.id == payload.tenant_id))
	tenant_obj = tenant_result.scalars().first()

	if tenant_obj is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Арендатор не найден")

	contract_obj = Contract(
		property_id=payload.property_id,
		tenant_id=payload.tenant_id,
		start_date=payload.start_date,
		end_date=payload.end_date,
		monthly_payment=payload.monthly_payment,
		security_deposit=payload.security_deposit,
		status=payload.status,
	)

	db.add(contract_obj)
	await db.commit()
	await db.refresh(contract_obj)

	return ContractResponse.model_validate(contract_obj)


@router.get("/{contract_id}", response_model=ContractResponse)
async def get_contract(
	contract_id: int,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> ContractResponse:
	"""Получить один договор, если он доступен пользователю."""
	contract_obj = await _get_contract_with_access(contract_id, current_user, db)
	return ContractResponse.model_validate(contract_obj)


@router.put("/{contract_id}", response_model=ContractResponse)
async def update_contract(
	contract_id: int,
	payload: ContractUpdate,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> ContractResponse:
	"""Обновить договор. Изменять может только владелец объекта."""
	contract_obj = await _get_owned_contract(contract_id, current_user, db)

	updates = payload.model_dump(exclude_unset=True)
	for field, value in updates.items():
		setattr(contract_obj, field, value)

	await db.commit()
	await db.refresh(contract_obj)
	return ContractResponse.model_validate(contract_obj)


@router.delete("/{contract_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contract(
	contract_id: int,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> Response:
	"""Удалить договор. Доступно только владельцу объекта."""
	contract_obj = await _get_owned_contract(contract_id, current_user, db)
	await db.delete(contract_obj)
	await db.commit()
	return Response(status_code=status.HTTP_204_NO_CONTENT)
