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
from app.services.payment_service import PaymentService


router = APIRouter(prefix="/payments", tags=["payments"])


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
	from app.services.contract_service import ContractService
	_, _ = await ContractService.get_with_access(contract_id, current_user.id, db)

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
	from app.services.contract_service import ContractService
	contract_obj, _ = await ContractService.get_with_access(payload.contract_id, current_user.id, db)
	payment_obj = await PaymentService.create_payment_for_owner(
		contract=contract_obj,
		owner_id=current_user.id,
		amount=payload.amount,
		due_date=payload.due_date,
		status=payload.status,
		comment=payload.comment,
		db=db,
	)
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
	payment_obj, _ = await PaymentService.get_with_access(payment_id, current_user.id, db)
	return PaymentResponse.model_validate(payment_obj)


@router.put("/{payment_id}", response_model=PaymentResponse)
async def update_payment(
	payment_id: int,
	payload: PaymentUpdate,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> PaymentResponse:
	"""Обновить платёж. Изменять может владелец объекта."""
	payment_obj = await PaymentService.get_owned(payment_id, current_user.id, db)

	updates = payload.model_dump(exclude_unset=True)
	for field, value in updates.items():
		setattr(payment_obj, field, value)

	if 'status' in updates:
		payment_obj = await PaymentService.update_payment_status(payment_obj, updates['status'], db)

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
	payment_obj = await PaymentService.get_owned(payment_id, current_user.id, db)
	await db.delete(payment_obj)
	await db.commit()
	return Response(status_code=status.HTTP_204_NO_CONTENT)
