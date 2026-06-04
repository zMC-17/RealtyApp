"""Роутер для заявок на обслуживание."""

from typing import Annotated, List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.request import (
    RequestCreate,
    RequestResponse,
    RequestUpdate,
    RequestWithDetailsResponse,
)
from app.services.request_service import RequestService

router = APIRouter(prefix="/requests", tags=["requests"])


def _build_details_dict(req) -> dict:
    """Вспомогательная функция для построения расширенного ответа."""
    req_dict = RequestResponse.model_validate(req).model_dump()

    contract = req.contract
    property_obj = contract.property

    req_dict["contract_info"] = {
        "id": contract.id,
        "start_date": contract.start_date,
        "end_date": contract.end_date,
        "monthly_payment": str(contract.monthly_payment),
    }
    req_dict["property_info"] = {
        "id": property_obj.id,
        "title": property_obj.title,
        "address": property_obj.address,
    }

    return req_dict


def _add_tenant_info(req_dict: dict, contract) -> dict:
    """Добавить информацию об арендаторе (для владельца)."""
    tenant = contract.tenant
    req_dict["tenant_info"] = {
        "id": tenant.id,
        "name": tenant.name,
        "email": tenant.email,
    }
    return req_dict


def _add_owner_info(req_dict: dict, property_obj) -> dict:
    """Добавить информацию о владельце (для арендатора)."""
    owner = property_obj.owner
    req_dict["owner_info"] = {
        "id": owner.id,
        "name": owner.name,
        "email": owner.email,
    }
    return req_dict


@router.get("/me", response_model=list[RequestResponse])
async def list_my_requests(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[RequestResponse]:
    """Все заявки текущего пользователя."""
    requests_list = await RequestService.list_related_requests(current_user.id, db)
    return [RequestResponse.model_validate(item) for item in requests_list]


@router.get("/owner/me", response_model=List[RequestWithDetailsResponse])
async def list_my_owner_requests(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> List[RequestWithDetailsResponse]:
    """Заявки по объектам текущего владельца с расширенной информацией."""
    requests = await RequestService.list_owner_requests(current_user.id, db)

    result = []
    for req in requests:
        req_dict = _build_details_dict(req)
        req_dict = _add_tenant_info(req_dict, req.contract)
        result.append(RequestWithDetailsResponse(**req_dict))

    return result


@router.get("/tenant/me", response_model=List[RequestWithDetailsResponse])
async def list_my_tenant_requests(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> List[RequestWithDetailsResponse]:
    """Заявки текущего арендатора с расширенной информацией."""
    requests = await RequestService.list_tenant_requests(current_user.id, db)

    result = []
    for req in requests:
        req_dict = _build_details_dict(req)
        req_dict = _add_owner_info(req_dict, req.contract.property)
        result.append(RequestWithDetailsResponse(**req_dict))

    return result


@router.get("/contracts/{contract_id}", response_model=list[RequestResponse])
async def list_contract_requests(
    contract_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[RequestResponse]:
    """Заявки по конкретному договору."""
    requests_list = await RequestService.list_contract_requests(
        contract_id, current_user.id, db
    )
    return [RequestResponse.model_validate(item) for item in requests_list]


@router.post(
    "", response_model=RequestWithDetailsResponse, status_code=status.HTTP_201_CREATED
)
async def create_request(
    payload: RequestCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RequestWithDetailsResponse:
    """Создать заявку. Доступно только арендатору активного договора."""
    req = await RequestService.create_request(payload, current_user.id, db)

    req_dict = _build_details_dict(req)
    req_dict = _add_owner_info(req_dict, req.contract.property)

    return RequestWithDetailsResponse(**req_dict)


@router.get("/{request_id}", response_model=RequestResponse)
async def get_request(
    request_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RequestResponse:
    """Получить заявку по ID."""
    request_obj, _ = await RequestService.get_with_access(
        request_id, current_user.id, db
    )
    return RequestResponse.model_validate(request_obj)


@router.put("/{request_id}", response_model=RequestWithDetailsResponse)
async def update_request(
    request_id: int,
    payload: RequestUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RequestWithDetailsResponse:
    """Обновить заявку. Изменять может владелец объекта."""
    req = await RequestService.update_request(request_id, current_user.id, db, payload)

    req_dict = _build_details_dict(req)
    req_dict = _add_tenant_info(req_dict, req.contract)

    return RequestWithDetailsResponse(**req_dict)


@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_request(
    request_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Response:
    """Удалить заявку. Доступно владельцу объекта."""
    await RequestService.delete_request(request_id, current_user.id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
