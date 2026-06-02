"""Роутер для платежей."""
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.payment import (
	ContractInfo,
	PaymentConfirmationRequest,
	PaymentCreate,
	PaymentResponse,
	PaymentUpdate,
	PaymentWithDetailsResponse,
	PropertyInfo,
	TenantInfo,
)
from app.services.payment_service import PaymentService


router = APIRouter(prefix="/payments", tags=["payments"])


@router.get("/me", response_model=list[PaymentWithDetailsResponse])
async def list_my_payments(
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> list[PaymentWithDetailsResponse]:
	"""Все платежи, связанные с текущим пользователем."""
	payments = await PaymentService.list_related_payments(current_user.id, db)

	result = []
	for payment in payments:
		payment_dict = PaymentResponse.model_validate(payment).model_dump()

		# Добавляем информацию о договоре
		contract = payment.contract
		payment_dict["contract_info"] = ContractInfo.model_validate(contract).model_dump()

		# Добавляем информацию об объекте
		property_obj = contract.property
		payment_dict["property_info"] = PropertyInfo.model_validate(property_obj).model_dump()

		# Добавляем информацию об арендаторе
		tenant = contract.tenant
		payment_dict["tenant_info"] = TenantInfo.model_validate(tenant).model_dump()

		result.append(PaymentWithDetailsResponse(**payment_dict))

	return result


@router.get("/owner/me", response_model=list[PaymentWithDetailsResponse])
async def list_my_owner_payments(
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> list[PaymentWithDetailsResponse]:
	"""Платежи по объектам текущего владельца с расширенной информацией."""
	payments = await PaymentService.list_owner_payments(current_user.id, db)

	result = []
	for payment in payments:
		payment_dict = PaymentResponse.model_validate(payment).model_dump()

		# Добавляем информацию о договоре
		contract = payment.contract
		payment_dict["contract_info"] = ContractInfo.model_validate(contract).model_dump()

		# Добавляем информацию об объекте
		property_obj = contract.property
		payment_dict["property_info"] = PropertyInfo.model_validate(property_obj).model_dump()

		# Добавляем информацию об арендаторе
		tenant = contract.tenant
		payment_dict["tenant_info"] = TenantInfo.model_validate(tenant).model_dump()

		result.append(PaymentWithDetailsResponse(**payment_dict))

	return result


@router.get("/tenant/me", response_model=list[PaymentWithDetailsResponse])
async def list_my_tenant_payments(
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> list[PaymentWithDetailsResponse]:
	"""Платежи текущего арендатора с расширенной информацией."""
	payments = await PaymentService.list_tenant_payments(current_user.id, db)

	result = []
	for payment in payments:
		payment_dict = PaymentResponse.model_validate(payment).model_dump()

		# Добавляем информацию о договоре
		contract = payment.contract
		payment_dict["contract_info"] = ContractInfo.model_validate(contract).model_dump()

		# Добавляем информацию об объекте
		property_obj = contract.property
		payment_dict["property_info"] = PropertyInfo.model_validate(property_obj).model_dump()

		# Добавляем информацию об арендаторе
		tenant = contract.tenant
		payment_dict["tenant_info"] = TenantInfo.model_validate(tenant).model_dump()

		result.append(PaymentWithDetailsResponse(**payment_dict))

	return result


@router.get("/contracts/{contract_id}", response_model=list[PaymentWithDetailsResponse])
async def list_contract_payments(
	contract_id: int,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> list[PaymentWithDetailsResponse]:
	"""Платежи по одному договору с расширенной информацией."""
	payments = await PaymentService.list_contract_payments(contract_id, current_user.id, db)

	result = []
	for payment in payments:
		payment_dict = PaymentResponse.model_validate(payment).model_dump()

		# Добавляем информацию о договоре
		contract = payment.contract
		payment_dict["contract_info"] = ContractInfo.model_validate(contract).model_dump()

		# Добавляем информацию об объекте
		property_obj = contract.property
		payment_dict["property_info"] = PropertyInfo.model_validate(property_obj).model_dump()

		# Добавляем информацию об арендаторе
		tenant = contract.tenant
		payment_dict["tenant_info"] = TenantInfo.model_validate(tenant).model_dump()

		result.append(PaymentWithDetailsResponse(**payment_dict))

	return result


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
	payload: PaymentCreate,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> PaymentResponse:
	"""Создать платеж для договора. Доступно владельцу объекта."""
	payment_obj = await PaymentService.create_payment_for_owner(payload, current_user.id, db)
	return PaymentResponse.model_validate(payment_obj)


@router.post("/{payment_id}/request-confirmation", response_model=PaymentResponse)
async def request_payment_confirmation(
	payment_id: int,
	payload: PaymentConfirmationRequest,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> PaymentResponse:
	"""Арендатор отправляет чек на подтверждение оплаты."""
	payment_obj = await PaymentService.request_confirmation(payment_id, current_user.id, payload, db)
	return PaymentResponse.model_validate(payment_obj)


@router.post("/{payment_id}/confirm", response_model=PaymentResponse)
async def confirm_payment(
	payment_id: int,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> PaymentResponse:
	"""Владелец подтверждает оплату после проверки чека."""
	payment_obj = await PaymentService.confirm_payment(payment_id, current_user.id, db)
	return PaymentResponse.model_validate(payment_obj)


@router.post("/{payment_id}/reject", response_model=PaymentResponse)
async def reject_payment_confirmation(
	payment_id: int,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> PaymentResponse:
	"""Владелец отклоняет подтверждение и возвращает платёж в ожидание оплаты."""
	payment_obj = await PaymentService.reject_confirmation(payment_id, current_user.id, db)
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
	payment_obj = await PaymentService.update(payment_id, current_user.id, payload, db)
	return PaymentResponse.model_validate(payment_obj)


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment(
	payment_id: int,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> Response:
	"""Удалить платёж. Доступно владельцу объекта."""
	await PaymentService.delete(payment_id, current_user.id, db)
	return Response(status_code=status.HTTP_204_NO_CONTENT)
