"""Роутер для платежей."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.contract import Contract
from app.models.payment import Payment
from app.models.property import Property
from app.models.user import User
from app.schemas.payment import PaymentCreate, PaymentResponse, PaymentUpdate


router = APIRouter(prefix="/payments", tags=["payments"])


async def _get_contract_and_property(
	contract_id: int,
	db: AsyncSession,
) -> tuple[Contract, Property]:
	"""Получить договор и связанный объект."""
	contract_result = await db.execute(select(Contract).where(Contract.id == contract_id))
	contract_obj = contract_result.scalars().first()

	if contract_obj is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Договор не найден")

	property_result = await db.execute(select(Property).where(Property.id == contract_obj.property_id))
	property_obj = property_result.scalars().first()

	if property_obj is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объект по договору не найден")

	return contract_obj, property_obj


async def _get_payment_with_access(
	payment_id: int,
	current_user: User,
	db: AsyncSession,
) -> Payment:
	"""Получить платёж и проверить доступ к нему."""
	result = await db.execute(select(Payment).where(Payment.id == payment_id))
	payment_obj = result.scalars().first()

	if payment_obj is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Платёж не найден")

	contract_obj, property_obj = await _get_contract_and_property(payment_obj.contract_id, db)

	if current_user.id not in (contract_obj.tenant_id, property_obj.owner_id):
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа к этому платежу")

	return payment_obj


async def _list_payments_for_contracts(
	contract_ids: list[int],
	db: AsyncSession,
	status_filter: str | None = None,
) -> list[Payment]:
	"""Получить платежи по списку договоров."""
	if not contract_ids:
		return []

	stmt = select(Payment).where(Payment.contract_id.in_(contract_ids)).order_by(Payment.due_date.desc())
	if status_filter:
		stmt = stmt.where(Payment.status == status_filter)

	result = await db.execute(stmt)
	return [payment for payment in result.scalars().all()]


@router.get("/me", response_model=list[PaymentResponse])
async def list_my_payments(
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> list[PaymentResponse]:
	"""Все платежи, связанные с текущим пользователем."""
	contract_ids_result = await db.execute(
		select(Contract.id).join(Property).where((Contract.tenant_id == current_user.id) | (Property.owner_id == current_user.id))
	)
	contract_ids = list(contract_ids_result.scalars().all())
	payments = await _list_payments_for_contracts(contract_ids, db)
	return [PaymentResponse.model_validate(item) for item in payments]


@router.get("/owner/me", response_model=list[PaymentResponse])
async def list_my_owner_payments(
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> list[PaymentResponse]:
	"""Платежи по объектам текущего владельца."""
	contract_ids_result = await db.execute(
		select(Contract.id).join(Property).where(Property.owner_id == current_user.id)
	)
	contract_ids = list(contract_ids_result.scalars().all())
	payments = await _list_payments_for_contracts(contract_ids, db)
	return [PaymentResponse.model_validate(item) for item in payments]


@router.get("/tenant/me", response_model=list[PaymentResponse])
async def list_my_tenant_payments(
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> list[PaymentResponse]:
	"""Платежи текущего арендатора."""
	contract_ids_result = await db.execute(
		select(Contract.id).where(Contract.tenant_id == current_user.id)
	)
	contract_ids = list(contract_ids_result.scalars().all())
	payments = await _list_payments_for_contracts(contract_ids, db)
	return [PaymentResponse.model_validate(item) for item in payments]


@router.get("/contracts/{contract_id}", response_model=list[PaymentResponse])
async def list_contract_payments(
	contract_id: int,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> list[PaymentResponse]:
	"""Платежи по одному договору."""
	contract_obj, property_obj = await _get_contract_and_property(contract_id, db)

	if current_user.id not in (contract_obj.tenant_id, property_obj.owner_id):
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа к платежам этого договора")

	result = await db.execute(
		select(Payment).where(Payment.contract_id == contract_id).order_by(Payment.due_date.desc())
	)
	payments = list(result.scalars().all())
	return [PaymentResponse.model_validate(item) for item in payments]


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
	payload: PaymentCreate,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> PaymentResponse:
	"""Создать платеж для договора. Доступно владельцу объекта."""
	contract_obj, property_obj = await _get_contract_and_property(payload.contract_id, db)

	if property_obj.owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Создавать платежи может только владелец объекта")

	payment_obj = Payment(
		contract_id=payload.contract_id,
		amount=payload.amount,
		due_date=payload.due_date,
		status=payload.status,
		comment=payload.comment,
	)

	db.add(payment_obj)
	await db.commit()
	await db.refresh(payment_obj)
	return PaymentResponse.model_validate(payment_obj)


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
	payment_id: int,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> PaymentResponse:
	"""Получить платёж по ID."""
	payment_obj = await _get_payment_with_access(payment_id, current_user, db)
	return PaymentResponse.model_validate(payment_obj)


@router.put("/{payment_id}", response_model=PaymentResponse)
async def update_payment(
	payment_id: int,
	payload: PaymentUpdate,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> PaymentResponse:
	"""Обновить платёж. Изменять может владелец объекта."""
	payment_obj = await _get_payment_with_access(payment_id, current_user, db)
	contract_obj, property_obj = await _get_contract_and_property(payment_obj.contract_id, db)

	if property_obj.owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Изменять платёж может только владелец объекта")

	updates = payload.model_dump(exclude_unset=True)
	for field, value in updates.items():
		setattr(payment_obj, field, value)

	if payment_obj.status == "paid" and payment_obj.paid_at is None:
		from datetime import datetime, timezone

		payment_obj.paid_at = datetime.now(timezone.utc)

	await db.commit()
	await db.refresh(payment_obj)
	return PaymentResponse.model_validate(payment_obj)


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment(
	payment_id: int,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> Response:
	"""Удалить платёж. Доступно владельцу объекта."""
	payment_obj = await _get_payment_with_access(payment_id, current_user, db)
	_, property_obj = await _get_contract_and_property(payment_obj.contract_id, db)

	if property_obj.owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Удалять платёж может только владелец объекта")

	await db.delete(payment_obj)
	await db.commit()
	return Response(status_code=status.HTTP_204_NO_CONTENT)
