"""Сервис для работы с заявками (maintenance requests)."""

from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.request import Request as MaintenanceRequest
from app.models.contract import Contract
from app.models.property import Property
from app.schemas.request import RequestCreate, RequestUpdate


class RequestService:

    @staticmethod
    async def list_related_requests(
        user_id: int, db: AsyncSession
    ) -> List[MaintenanceRequest]:
        """Получить все заявки, связанные с пользователем."""
        from app.services.contract_service import ContractService

        contract_ids = []
        for contract in await ContractService.list_related_contracts(user_id, db):
            contract_ids.append(contract.id)

        return await RequestService._list_requests_for_contracts(contract_ids, db)

    @staticmethod
    async def list_owner_requests(
        owner_id: int, db: AsyncSession
    ) -> List[MaintenanceRequest]:
        """Получить все заявки по объектам владельца."""
        from app.services.contract_service import ContractService

        contract_ids = []
        for contract in await ContractService.list_owner_contracts(owner_id, db):
            contract_ids.append(contract.id)

        return await RequestService._list_requests_for_contracts(contract_ids, db)

    @staticmethod
    async def list_tenant_requests(
        tenant_id: int, db: AsyncSession
    ) -> List[MaintenanceRequest]:
        """Получить все заявки арендатора."""
        from app.services.contract_service import ContractService

        contract_ids = []
        for contract in await ContractService.list_tenant_contracts(tenant_id, db):
            contract_ids.append(contract.id)

        return await RequestService._list_requests_for_contracts(contract_ids, db)

    @staticmethod
    async def list_contract_requests(
        contract_id: int, user_id: int, db: AsyncSession
    ) -> List[MaintenanceRequest]:
        """Получить заявки по одному договору после проверки доступа."""
        from app.services.contract_service import ContractService

        await ContractService.get_with_access(contract_id, user_id, db)
        return await RequestService._list_requests_for_contracts([contract_id], db)

    @staticmethod
    async def _list_requests_for_contracts(
        contract_ids: list[int], db: AsyncSession
    ) -> List[MaintenanceRequest]:
        if not contract_ids:
            return []

        # ✅ ИСПРАВЛЕНО: Загружаем все связанные данные заранее
        stmt = (
            select(MaintenanceRequest)
            .where(MaintenanceRequest.contract_id.in_(contract_ids))
            .options(
                selectinload(MaintenanceRequest.contract)
                .selectinload(Contract.property)
                .selectinload(Property.owner),
                selectinload(MaintenanceRequest.contract).selectinload(Contract.tenant),
            )
            .order_by(MaintenanceRequest.created_at.desc())
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def create_request(
        payload: RequestCreate, tenant_user_id: int, db: AsyncSession
    ) -> MaintenanceRequest:
        """Создать заявку. Только арендатор активного договора."""
        # Проверяем что договор существует и принадлежит арендатору
        stmt = select(Contract).where(
            Contract.id == payload.contract_id,
            Contract.tenant_id == tenant_user_id,
            Contract.status == "active",
        )
        res = await db.execute(stmt)
        contract = res.scalars().first()

        if contract is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Активный договор не найден или вы не являетесь его арендатором",
            )

        req = MaintenanceRequest(
            contract_id=payload.contract_id,
            title=payload.title,
            message=payload.message,
            status=payload.status,
        )
        db.add(req)
        await db.flush()

        # ✅ ИСПРАВЛЕНО: Загружаем связанные данные после создания
        await db.refresh(req, attribute_names=["contract"])
        await db.refresh(req.contract, attribute_names=["property", "tenant"])
        if req.contract and req.contract.property:
            await db.refresh(req.contract.property, attribute_names=["owner"])

        await db.commit()
        return req

    @staticmethod
    async def update_request(
        request_id: int, owner_id: int, db: AsyncSession, payload: RequestUpdate
    ) -> MaintenanceRequest:
        """Обновить заявку и сразу сохранить изменения."""
        request_obj = await RequestService.get_owned(request_id, owner_id, db)
        updates = payload.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(request_obj, field, value)
        await db.flush()
        await db.commit()

        # ✅ ИСПРАВЛЕНО: Загружаем связанные данные после обновления
        await db.refresh(request_obj, attribute_names=["contract"])
        if request_obj.contract:
            await db.refresh(
                request_obj.contract, attribute_names=["property", "tenant"]
            )
            if request_obj.contract.property:
                await db.refresh(
                    request_obj.contract.property, attribute_names=["owner"]
                )

        return request_obj

    @staticmethod
    async def delete_request(request_id: int, owner_id: int, db: AsyncSession) -> None:
        """Удалить заявку и сохранить удаление."""
        request_obj = await RequestService.get_owned(request_id, owner_id, db)
        await db.delete(request_obj)
        await db.commit()

    @staticmethod
    async def get_with_access(
        request_id: int, user_id: int, db: AsyncSession
    ) -> tuple[MaintenanceRequest, int]:
        """Получить заявку и проверить доступ (владелец или арендатор).

        Returns:
            tuple[Request, owner_id]: заявка и ID владельца объекта
        """
        # ✅ ИСПРАВЛЕНО: Загружаем связанные данные
        stmt = (
            select(MaintenanceRequest)
            .where(MaintenanceRequest.id == request_id)
            .options(
                selectinload(MaintenanceRequest.contract)
                .selectinload(Contract.property)
                .selectinload(Property.owner),
                selectinload(MaintenanceRequest.contract).selectinload(Contract.tenant),
            )
        )
        result = await db.execute(stmt)
        request_obj = result.scalars().first()

        if request_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Заявка не найдена"
            )

        contract = request_obj.contract
        if contract is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Договор не найден"
            )

        prop = contract.property
        if prop is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Объект не найден"
            )

        if user_id not in (contract.tenant_id, prop.owner_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Нет доступа к этой заявке",
            )

        return request_obj, prop.owner_id

    @staticmethod
    async def get_owned(
        request_id: int, owner_id: int, db: AsyncSession
    ) -> MaintenanceRequest:
        """Получить заявку только для владельца объекта."""
        request_obj, prop_owner_id = await RequestService.get_with_access(
            request_id, owner_id, db
        )
        if prop_owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Только владелец может изменять заявки",
            )
        return request_obj
