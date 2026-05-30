"""Сервис для работы с договорами и генерации платежей."""
from datetime import date
import calendar
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contract import Contract
from app.models.property import Property
from app.models.user import User
from app.schemas.contract import ContractCreate, ContractUpdate
from app.services.payment_service import PaymentService


def _add_months(orig_date: date, months: int) -> date:
	year = orig_date.year + (orig_date.month - 1 + months) // 12
	month = (orig_date.month - 1 + months) % 12 + 1
	day = orig_date.day
	last_day = calendar.monthrange(year, month)[1]
	return date(year, month, min(day, last_day))


class ContractService:
	@staticmethod
	async def create_contract(payload: ContractCreate, owner_user: User, db: AsyncSession) -> Contract:
		# Verify property exists and belongs to owner
		prop_stmt = select(Property).where(Property.id == payload.property_id)
		prop_res = await db.execute(prop_stmt)
		prop = prop_res.scalars().first()

		if prop is None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объект не найден")

		if prop.owner_id != owner_user.id:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Создавать договор может только владелец объекта")

		# Verify tenant exists
		tenant_stmt = select(User).where(User.id == payload.tenant_id)
		tenant_res = await db.execute(tenant_stmt)
		tenant = tenant_res.scalars().first()
		if tenant is None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Арендатор не найден")

		contract_obj = Contract(
			property_id=payload.property_id,
			tenant_id=payload.tenant_id,
			start_date=payload.start_date,
			end_date=payload.end_date,
			monthly_payment=payload.monthly_payment,
			security_deposit=payload.security_deposit,
			status=payload.status,
		)

		db.add(contract_obj)
		await db.flush()  # ensure contract_obj.id

		# Generate monthly payments (MVP: create a payment for each month between start and end inclusive)
		await PaymentService.generate_payments_for_contract(contract_obj, db)

		return contract_obj

	@staticmethod
	async def get_with_access(contract_id: int, user_id: int, db: AsyncSession) -> tuple[Contract, int]:
		"""Получить договор и проверить доступ (владелец или арендатор).

		Returns:
			tuple[Contract, owner_id]: договор и ID владельца объекта
		"""
		stmt = select(Contract).join(Property).where(Contract.id == contract_id)
		result = await db.execute(stmt)
		contract = result.scalars().first()

		if contract is None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Договор не найден")

		prop_stmt = select(Property.owner_id).where(Property.id == contract.property_id)
		prop_result = await db.execute(prop_stmt)
		owner_id = prop_result.scalar_one_or_none()

		if owner_id is None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объект по договору не найден")

		if user_id not in (contract.tenant_id, owner_id):
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа к этому договору")

		return contract, owner_id

	@staticmethod
	async def get_owned(contract_id: int, owner_id: int, db: AsyncSession) -> Contract:
		"""Получить договор только если текущий пользователь - владелец объекта."""
		contract, prop_owner_id = await ContractService.get_with_access(contract_id, owner_id, db)
		if prop_owner_id != owner_id:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Только владелец может изменять этот договор")
		return contract
