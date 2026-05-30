"""Роутер для заявок на обслуживание."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.contract import Contract
from app.models.property import Property
from app.models.request import Request as MaintenanceRequest
from app.models.user import User
from app.schemas.request import RequestCreate, RequestResponse, RequestUpdate


router = APIRouter(prefix="/requests", tags=["requests"])


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


async def _get_request_with_access(
	request_id: int,
	current_user: User,
	db: AsyncSession,
) -> MaintenanceRequest:
	"""Получить заявку и проверить доступ."""
	result = await db.execute(select(MaintenanceRequest).where(MaintenanceRequest.id == request_id))
	request_obj = result.scalars().first()

	if request_obj is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заявка не найдена")

	contract_obj, property_obj = await _get_contract_and_property(request_obj.contract_id, db)

	if current_user.id not in (contract_obj.tenant_id, property_obj.owner_id):
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа к этой заявке")

	return request_obj


async def _list_requests_for_contracts(
	contract_ids: list[int],
	db: AsyncSession,
	status_filter: str | None = None,
) -> list[MaintenanceRequest]:
	"""Получить заявки по списку договоров."""
	if not contract_ids:
		return []

	stmt = select(MaintenanceRequest).where(MaintenanceRequest.contract_id.in_(contract_ids)).order_by(MaintenanceRequest.created_at.desc())
	if status_filter:
		stmt = stmt.where(MaintenanceRequest.status == status_filter)

	result = await db.execute(stmt)
	return [request_item for request_item in result.scalars().all()]


@router.get("/me", response_model=list[RequestResponse])
async def list_my_requests(
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> list[RequestResponse]:
	"""Все заявки текущего пользователя."""
	contract_ids_result = await db.execute(
		select(Contract.id).join(Property).where((Contract.tenant_id == current_user.id) | (Property.owner_id == current_user.id))
	)
	contract_ids = list(contract_ids_result.scalars().all())
	requests_list = await _list_requests_for_contracts(contract_ids, db)
	return [RequestResponse.model_validate(item) for item in requests_list]


@router.get("/owner/me", response_model=list[RequestResponse])
async def list_my_owner_requests(
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> list[RequestResponse]:
	"""Заявки по объектам текущего владельца."""
	contract_ids_result = await db.execute(
		select(Contract.id).join(Property).where(Property.owner_id == current_user.id)
	)
	contract_ids = list(contract_ids_result.scalars().all())
	requests_list = await _list_requests_for_contracts(contract_ids, db)
	return [RequestResponse.model_validate(item) for item in requests_list]


@router.get("/tenant/me", response_model=list[RequestResponse])
async def list_my_tenant_requests(
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> list[RequestResponse]:
	"""Заявки текущего арендатора."""
	contract_ids_result = await db.execute(
		select(Contract.id).where(Contract.tenant_id == current_user.id)
	)
	contract_ids = list(contract_ids_result.scalars().all())
	requests_list = await _list_requests_for_contracts(contract_ids, db)
	return [RequestResponse.model_validate(item) for item in requests_list]


@router.get("/contracts/{contract_id}", response_model=list[RequestResponse])
async def list_contract_requests(
	contract_id: int,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> list[RequestResponse]:
	"""Заявки по конкретному договору."""
	contract_obj, property_obj = await _get_contract_and_property(contract_id, db)

	if current_user.id not in (contract_obj.tenant_id, property_obj.owner_id):
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа к заявкам этого договора")

	result = await db.execute(
		select(MaintenanceRequest).where(MaintenanceRequest.contract_id == contract_id).order_by(MaintenanceRequest.created_at.desc())
	)
	requests_list = list(result.scalars().all())
	return [RequestResponse.model_validate(item) for item in requests_list]


@router.post("", response_model=RequestResponse, status_code=status.HTTP_201_CREATED)
async def create_request(
	payload: RequestCreate,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> RequestResponse:
	"""Создать заявку. Доступно только арендатору договора."""
	contract_obj, _ = await _get_contract_and_property(payload.contract_id, db)

	if contract_obj.tenant_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Создавать заявку может только арендатор договора")

	request_obj = MaintenanceRequest(
		contract_id=payload.contract_id,
		message=payload.message,
		status=payload.status,
	)

	db.add(request_obj)
	await db.commit()
	await db.refresh(request_obj)
	return RequestResponse.model_validate(request_obj)


@router.get("/{request_id}", response_model=RequestResponse)
async def get_request(
	request_id: int,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> RequestResponse:
	"""Получить заявку по ID."""
	request_obj = await _get_request_with_access(request_id, current_user, db)
	return RequestResponse.model_validate(request_obj)


@router.put("/{request_id}", response_model=RequestResponse)
async def update_request(
	request_id: int,
	payload: RequestUpdate,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> RequestResponse:
	"""Обновить заявку. Изменять может владелец объекта."""
	request_obj = await _get_request_with_access(request_id, current_user, db)
	contract_obj, property_obj = await _get_contract_and_property(request_obj.contract_id, db)

	if property_obj.owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Изменять заявку может только владелец объекта")

	updates = payload.model_dump(exclude_unset=True)
	for field, value in updates.items():
		setattr(request_obj, field, value)

	await db.commit()
	await db.refresh(request_obj)
	return RequestResponse.model_validate(request_obj)


@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_request(
	request_id: int,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> Response:
	"""Удалить заявку. Доступно владельцу объекта."""
	request_obj = await _get_request_with_access(request_id, current_user, db)
	_, property_obj = await _get_contract_and_property(request_obj.contract_id, db)

	if property_obj.owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Удалять заявку может только владелец объекта")

	await db.delete(request_obj)
	await db.commit()
	return Response(status_code=status.HTTP_204_NO_CONTENT)
