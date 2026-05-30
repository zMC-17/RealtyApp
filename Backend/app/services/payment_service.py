"""Сервис для работы с платежами: создание, генерация расписания и обновление статуса."""
from datetime import date, datetime, timezone
import calendar
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contract import Contract
from app.models.payment import Payment
from app.models.property import Property
from app.models.user import User


def _add_months(orig_date: date, months: int) -> date:
	year = orig_date.year + (orig_date.month - 1 + months) // 12
	month = (orig_date.month - 1 + months) % 12 + 1
	day = orig_date.day
	last_day = calendar.monthrange(year, month)[1]
	return date(year, month, min(day, last_day))


class PaymentService:
	@staticmethod
	async def generate_payments_for_contract(contract: Contract, db: AsyncSession) -> List[Payment]:
		"""Generate monthly payments from contract.start_date to contract.end_date inclusive.

		This function only adds Payment objects to the session; caller is responsible for committing.
		"""
		payments: List[Payment] = []
		start = contract.start_date
		end = contract.end_date

		# Calculate number of months between start and end (inclusive)
		months = (end.year - start.year) * 12 + (end.month - start.month)

		for m in range(months + 1):
			due = _add_months(start, m)
			payment = Payment(
				contract_id=contract.id,
				amount=contract.monthly_payment,
				due_date=due,
				status="pending",
			)
			db.add(payment)
			payments.append(payment)

		return payments

	@staticmethod
	async def create_payment_for_owner(contract: Contract, owner_id: int, amount, due_date: date, status: str, comment: str | None, db: AsyncSession) -> Payment:
		# verify ownership
		prop_stmt = select(Property).where(Property.id == contract.property_id)
		prop_res = await db.execute(prop_stmt)
		prop = prop_res.scalars().first()
		if prop is None or prop.owner_id != owner_id:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Создавать платежи может только владелец объекта")

		payment = Payment(
			contract_id=contract.id,
			amount=amount,
			due_date=due_date,
			status=status,
			comment=comment,
		)
		db.add(payment)
		await db.flush()
		return payment

	@staticmethod
	async def update_payment_status(payment: Payment, new_status: str, db: AsyncSession) -> Payment:
		payment.status = new_status
		if new_status == "paid" and payment.paid_at is None:
			payment.paid_at = datetime.now(timezone.utc)
		await db.flush()
		return payment

	@staticmethod
	async def get_with_access(payment_id: int, user_id: int, db: AsyncSession) -> tuple[Payment, int]:
		"""Получить платёж и проверить доступ (владелец или арендатор).

		Returns:
			tuple[Payment, owner_id]: платёж и ID владельца объекта
		"""
		stmt = select(Payment).where(Payment.id == payment_id)
		result = await db.execute(stmt)
		payment = result.scalars().first()

		if payment is None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Платёж не найден")

		contract_stmt = select(Contract).where(Contract.id == payment.contract_id)
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
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа к этому платежу")

		return payment, prop.owner_id

	@staticmethod
	async def get_owned(payment_id: int, owner_id: int, db: AsyncSession) -> Payment:
		"""Получить платёж только для владельца объекта."""
		payment, prop_owner_id = await PaymentService.get_with_access(payment_id, owner_id, db)
		if prop_owner_id != owner_id:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Только владелец может изменять платежи")
		return payment
