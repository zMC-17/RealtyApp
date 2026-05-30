"""Сервис для работы с заявками (maintenance requests)."""
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.request import Request as MaintenanceRequest
from app.models.contract import Contract
from app.models.property import Property
from app.schemas.request import RequestCreate, RequestUpdate


class RequestService:
	@staticmethod
	async def list_related_requests(user_id: int, db: AsyncSession) -> List[MaintenanceRequest]:
		"""Получить все заявки, связанные с пользователем."""
		from app.services.contract_service import ContractService

		contract_ids = []
		for contract in await ContractService.list_related_contracts(user_id, db):
			contract_ids.append(contract.id)

		return await RequestService._list_requests_for_contracts(contract_ids, db)

	@staticmethod
	async def list_owner_requests(owner_id: int, db: AsyncSession) -> List[MaintenanceRequest]:
		"""Получить все заявки по объектам владельца."""
		from app.services.contract_service import ContractService

		contract_ids = []
		for contract in await ContractService.list_owner_contracts(owner_id, db):
			contract_ids.append(contract.id)

		return await RequestService._list_requests_for_contracts(contract_ids, db)

	@staticmethod
	async def list_tenant_requests(tenant_id: int, db: AsyncSession) -> List[MaintenanceRequest]:
		"""Получить все заявки арендатора."""
		from app.services.contract_service import ContractService

		contract_ids = []
		for contract in await ContractService.list_tenant_contracts(tenant_id, db):
			contract_ids.append(contract.id)

		return await RequestService._list_requests_for_contracts(contract_ids, db)

	@staticmethod
	async def list_contract_requests(contract_id: int, user_id: int, db: AsyncSession) -> List[MaintenanceRequest]:
		"""Получить заявки по одному договору после проверки доступа."""
		from app.services.contract_service import ContractService

		await ContractService.get_with_access(contract_id, user_id, db)
		return await RequestService._list_requests_for_contracts([contract_id], db)

	@staticmethod
	async def _list_requests_for_contracts(contract_ids: list[int], db: AsyncSession) -> List[MaintenanceRequest]:
		if not contract_ids:
			return []

		stmt = select(MaintenanceRequest).where(MaintenanceRequest.contract_id.in_(contract_ids)).order_by(MaintenanceRequest.created_at.desc())
		result = await db.execute(stmt)
		return list(result.scalars().all())

	@staticmethod
	async def create_request(payload: RequestCreate, tenant_user_id: int, db: AsyncSession) -> MaintenanceRequest:
		# Verify contract exists and tenant is the contract tenant
		stmt = select(Contract).where(Contract.id == payload.contract_id)
		res = await db.execute(stmt)
		contract = res.scalars().first()
		if contract is None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Договор не найден")

		if contract.tenant_id != tenant_user_id:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Создавать заявку может только арендатор договора")

		req = MaintenanceRequest(
			contract_id=payload.contract_id,
			message=payload.message,
			status=payload.status,
		)
		db.add(req)
		await db.flush()
		await db.commit()
		await db.refresh(req)
		return req

	@staticmethod
	async def update_request(request_id: int, owner_id: int, db: AsyncSession, payload: RequestUpdate) -> MaintenanceRequest:
		"""Обновить заявку и сразу сохранить изменения."""
		request_obj = await RequestService.get_owned(request_id, owner_id, db)
		updates = payload.model_dump(exclude_unset=True)
		for field, value in updates.items():
			setattr(request_obj, field, value)
		await db.flush()
		await db.commit()
		await db.refresh(request_obj)
		return request_obj

	@staticmethod
	async def delete_request(request_id: int, owner_id: int, db: AsyncSession) -> None:
		"""Удалить заявку и сохранить удаление."""
		request_obj = await RequestService.get_owned(request_id, owner_id, db)
		await db.delete(request_obj)
		await db.commit()

	@staticmethod
	async def get_with_access(request_id: int, user_id: int, db: AsyncSession) -> tuple[MaintenanceRequest, int]:
		"""Получить заявку и проверить доступ (владелец или арендатор).

		Returns:
			tuple[Request, owner_id]: заявка и ID владельца объекта
		"""
		stmt = select(MaintenanceRequest).where(MaintenanceRequest.id == request_id)
		result = await db.execute(stmt)
		request_obj = result.scalars().first()

		if request_obj is None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заявка не найдена")

		contract_stmt = select(Contract).where(Contract.id == request_obj.contract_id)
		contract_result = await db.execute(contract_stmt)
		contract = contract_result.scalars().first()

		if contract is None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Договор не найден")

		prop_stmt = select(Property).where(Property.id == contract.property_id)
		prop_result = await db.execute(prop_stmt)
		prop = prop_result.scalars().first()

		if prop is None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объект не найден")

		if user_id not in (contract.tenant_id, prop.owner_id):
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа к этой заявке")

		return request_obj, prop.owner_id

	@staticmethod
	async def get_owned(request_id: int, owner_id: int, db: AsyncSession) -> MaintenanceRequest:
		"""Получить заявку только для владельца объекта."""
		request_obj, prop_owner_id = await RequestService.get_with_access(request_id, owner_id, db)
		if prop_owner_id != owner_id:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Только владелец может изменять заявки")
		return request_obj
