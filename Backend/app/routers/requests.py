"""Роутер для заявок на обслуживание."""
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.request import RequestCreate, RequestResponse, RequestUpdate
from app.services.request_service import RequestService


router = APIRouter(prefix="/requests", tags=["requests"])


@router.get("/me", response_model=list[RequestResponse])
async def list_my_requests(
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> list[RequestResponse]:
	"""Все заявки текущего пользователя."""
	requests_list = await RequestService.list_related_requests(current_user.id, db)
	return [RequestResponse.model_validate(item) for item in requests_list]


@router.get("/owner/me", response_model=list[RequestResponse])
async def list_my_owner_requests(
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> list[RequestResponse]:
	"""Заявки по объектам текущего владельца."""
	requests_list = await RequestService.list_owner_requests(current_user.id, db)
	return [RequestResponse.model_validate(item) for item in requests_list]


@router.get("/tenant/me", response_model=list[RequestResponse])
async def list_my_tenant_requests(
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> list[RequestResponse]:
	"""Заявки текущего арендатора."""
	requests_list = await RequestService.list_tenant_requests(current_user.id, db)
	return [RequestResponse.model_validate(item) for item in requests_list]


@router.get("/contracts/{contract_id}", response_model=list[RequestResponse])
async def list_contract_requests(
	contract_id: int,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> list[RequestResponse]:
	"""Заявки по конкретному договору."""
	requests_list = await RequestService.list_contract_requests(contract_id, current_user.id, db)
	return [RequestResponse.model_validate(item) for item in requests_list]


@router.post("", response_model=RequestResponse, status_code=status.HTTP_201_CREATED)
async def create_request(
	payload: RequestCreate,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> RequestResponse:
	"""Создать заявку. Доступно только арендатору договора."""
	request_obj = await RequestService.create_request(payload, current_user.id, db)
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
	request_obj = await RequestService.update_request(request_id, current_user.id, db, payload)
	return RequestResponse.model_validate(request_obj)


@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_request(
	request_id: int,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Annotated[AsyncSession, Depends(get_db)],
) -> Response:
	"""Удалить заявку. Доступно владельцу объекта."""
	await RequestService.delete_request(request_id, current_user.id, db)
	return Response(status_code=status.HTTP_204_NO_CONTENT)
