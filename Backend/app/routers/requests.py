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
from app.services.request_service import RequestService


router = APIRouter(prefix="/requests", tags=["requests"])


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
	from app.services.contract_service import ContractService
	_, _ = await ContractService.get_with_access(contract_id, current_user.id, db)

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
	request_obj = await RequestService.create_request(payload, current_user.id, db)
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
	request_obj, _ = await RequestService.get_with_access(request_id, current_user.id, db)
	return RequestResponse.model_validate(request_obj)


@router.put("/{request_id}", response_model=RequestResponse)
async def update_request(
	request_id: int,
	payload: RequestUpdate,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> RequestResponse:
	"""Обновить заявку. Изменять может владелец объекта."""
	request_obj = await RequestService.get_owned(request_id, current_user.id, db)
	request_obj = await RequestService.update_request(request_obj, current_user.id, db, payload)
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
	request_obj = await RequestService.get_owned(request_id, current_user.id, db)
	await RequestService.delete_request(request_obj, current_user.id, db)
	await db.commit()
	return Response(status_code=status.HTTP_204_NO_CONTENT)
