"""Роутер для договоров аренды."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.contract import (
    ContractCreate,
    ContractCreateByEmail,
    ContractResponse,
    ContractUpdate,
    ContractWithDetailsResponse,
    OwnerInfo,
    PropertyInfo,
)
from app.services.contract_service import ContractService

router = APIRouter(prefix="/contracts", tags=["contracts"])


@router.get("/me", response_model=list[ContractResponse])
async def list_my_contracts(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[ContractResponse]:
    """Все договоры, связанные с текущим пользователем."""
    contracts = await ContractService.list_related_contracts(current_user.id, db)
    return [ContractResponse.model_validate(item) for item in contracts]


@router.get("/owner/me", response_model=list[ContractResponse])
async def list_my_owner_contracts(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[ContractResponse]:
    """Договоры по объектам текущего владельца."""
    contracts = await ContractService.list_owner_contracts(current_user.id, db)
    return [ContractResponse.model_validate(item) for item in contracts]


@router.get("/tenant/me", response_model=list[ContractWithDetailsResponse])
async def list_my_tenant_contracts(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[ContractWithDetailsResponse]:
    """Договоры текущего арендатора с расширенной информацией."""
    contracts = await ContractService.list_tenant_contracts(current_user.id, db)

    result: list[ContractWithDetailsResponse] = []
    for contract in contracts:
        contract_dict = ContractResponse.model_validate(contract).model_dump()

        property_obj = contract.property
        contract_dict["property_info"] = (
            PropertyInfo.model_validate(property_obj, from_attributes=True).model_dump()
            if property_obj
            else None
        )

        owner = property_obj.owner if property_obj else None
        contract_dict["owner_info"] = (
            OwnerInfo.model_validate(owner, from_attributes=True).model_dump()
            if owner
            else None
        )

        result.append(ContractWithDetailsResponse(**contract_dict))

    return result


@router.post("", response_model=ContractResponse, status_code=status.HTTP_201_CREATED)
async def create_contract(
    payload: ContractCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ContractResponse:
    """Создать договор аренды для объекта текущего владельца."""
    contract_obj = await ContractService.create_contract(payload, current_user, db)
    return ContractResponse.model_validate(contract_obj)


@router.post(
    "/by-email", response_model=ContractResponse, status_code=status.HTTP_201_CREATED
)
async def create_contract_by_email(
    payload: ContractCreateByEmail,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ContractResponse:
    """Создать договор аренды по email арендатора."""
    contract_obj = await ContractService.create_contract_by_email(
        payload, current_user, db
    )
    return ContractResponse.model_validate(contract_obj)


@router.get("/{contract_id}", response_model=ContractResponse)
async def get_contract(
    contract_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ContractResponse:
    """Получить один договор, если он доступен пользователю."""
    contract_obj, _ = await ContractService.get_with_access(
        contract_id, current_user.id, db
    )
    return ContractResponse.model_validate(contract_obj)


@router.post("/{contract_id}/confirm", response_model=ContractResponse)
async def confirm_contract(
    contract_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ContractResponse:
    """Арендатор подтверждает договор. После этого генерируются платежи."""
    contract_obj = await ContractService.confirm_contract(
        contract_id, current_user.id, db
    )
    return ContractResponse.model_validate(contract_obj)


@router.put("/{contract_id}", response_model=ContractResponse)
async def update_contract(
    contract_id: int,
    payload: ContractUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ContractResponse:
    """Обновить договор. Изменять может только владелец объекта."""
    contract_obj = await ContractService.update(
        contract_id, current_user.id, payload, db
    )
    return ContractResponse.model_validate(contract_obj)


@router.delete("/{contract_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contract(
    contract_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Response:
    """Удалить договор. Доступно только владельцу объекта."""
    await ContractService.delete(contract_id, current_user.id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
