import calendar
from datetime import date, datetime, timezone
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contract import Contract
from app.models.payment import Payment
from app.models.property import Property
from app.schemas.payment import PaymentConfirmationRequest, PaymentCreate, PaymentUpdate


PAYMENT_ALLOWED_STATUSES = {"pending", "waiting_confirmation", "overdue", "paid"}
PAYMENT_TRANSITIONS = {
	"pending": {"waiting_confirmation", "overdue"},
	"waiting_confirmation": {"pending", "overdue", "paid"},
	"overdue": {"waiting_confirmation", "paid"},
	"paid": set(),
}


def _add_months(orig_date: date, months: int) -> date:
	"""Прибавить месяцы к дате, обработав конец месяца.

	Пример: 31.01 + 1 месяц = 28.02 (не 31, т.к. февраля нет)
	"""
	year = orig_date.year + (orig_date.month - 1 + months) // 12
	month = (orig_date.month - 1 + months) % 12 + 1
	day = orig_date.day
	last_day = calendar.monthrange(year, month)[1]
	return date(year, month, min(day, last_day))


class PaymentService:
	@staticmethod
	async def list_related_payments(user_id: int, db: AsyncSession) -> List[Payment]:
		"""Получить все платежи, связанные с пользователем как с арендатором или владельцем."""
		from app.services.contract_service import ContractService

		contract_ids = []
		for contract in await ContractService.list_related_contracts(user_id, db):
			contract_ids.append(contract.id)

		return await PaymentService._list_payments_for_contracts(contract_ids, db)

	@staticmethod
	async def list_owner_payments(owner_id: int, db: AsyncSession) -> List[Payment]:
		"""Получить все платежи по объектам владельца."""
		from app.services.contract_service import ContractService

		contract_ids = []
		for contract in await ContractService.list_owner_contracts(owner_id, db):
			contract_ids.append(contract.id)

		return await PaymentService._list_payments_for_contracts(contract_ids, db)

	@staticmethod
	async def list_tenant_payments(tenant_id: int, db: AsyncSession) -> List[Payment]:
		"""Получить все платежи арендатора."""
		from app.services.contract_service import ContractService

		contract_ids = []
		for contract in await ContractService.list_tenant_contracts(tenant_id, db):
			contract_ids.append(contract.id)

		return await PaymentService._list_payments_for_contracts(contract_ids, db)

	@staticmethod
	async def list_contract_payments(contract_id: int, user_id: int, db: AsyncSession) -> List[Payment]:
		"""Получить платежи по одному договору после проверки доступа."""
		from app.services.contract_service import ContractService

		await ContractService.get_with_access(contract_id, user_id, db)
		return await PaymentService._list_payments_for_contracts([contract_id], db)

	@staticmethod
	async def _list_payments_for_contracts(contract_ids: list[int], db: AsyncSession) -> List[Payment]:
		if not contract_ids:
			return []

		stmt = (
			select(Payment)
			.where(Payment.contract_id.in_(contract_ids))
			.options(
				selectinload(Payment.contract).selectinload(Contract.property),
				selectinload(Payment.contract).selectinload(Contract.tenant)
			)
			.order_by(Payment.due_date.desc())
		)
		result = await db.execute(stmt)
		return list(result.scalars().unique().all())

	@staticmethod
	async def _load_payment_context(payment_id: int, db: AsyncSession) -> tuple[Payment, Contract, int]:
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

		return payment, contract, prop.owner_id

	@staticmethod
	def _validate_transition(current_status: str, new_status: str) -> None:
		if new_status not in PAYMENT_ALLOWED_STATUSES:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Недопустимый статус платежа")

		allowed_transitions = PAYMENT_TRANSITIONS.get(current_status, set())
		if new_status not in allowed_transitions and new_status != current_status:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Недопустимый переход статуса платежа")

	@staticmethod
	async def _apply_status(payment: Payment, new_status: str, db: AsyncSession) -> Payment:
		PaymentService._validate_transition(payment.status, new_status)
		payment.status = new_status

		if new_status == "paid":
			payment.paid_at = datetime.now(timezone.utc)
		elif new_status != "waiting_confirmation":
			payment.paid_at = None

		await db.flush()
		return payment

	@staticmethod
	async def generate_payments_for_contract(contract: Contract, db: AsyncSession) -> List[Payment]:
		"""Создать платежи на каждый месяц договора (с start_date до end_date включительно).

		Алгоритм:
		1. Считаем кол-во месяцев между start_date и end_date
		2. Для каждого месяца создаём Payment с due_date на первый день месяца
		3. Сумма = contract.monthly_payment, статус = 'pending'

		Пример: договор 2024-01-15 до 2024-03-20
		- Платёж 1: 2024-01-15 (первый месяц)
		- Платёж 2: 2024-02-15 (второй месяц)
		- Платёж 3: 2024-03-15 (третий месяц)
		"""
		payments: List[Payment] = []
		start = contract.start_date
		end = contract.end_date

		# Считаем месяцы: (конец_год - нач_год) * 12 + (конец_месяц - нач_месяц)
		months = (end.year - start.year) * 12 + (end.month - start.month)

		for m in range(months + 1):
			# Прибавляем m месяцев к start_date
			due = _add_months(start, m)
			payment = Payment(
				contract_id=contract.id,
				amount=contract.monthly_payment,
				due_date=due,
				status="pending",
				payment_proof_url=None,
				confirmation_requested_at=None,
			)
			db.add(payment)
			payments.append(payment)

		return payments

	@staticmethod
	async def create_payment_for_owner(payload: PaymentCreate, owner_id: int, db: AsyncSession) -> Payment:
		"""Создать платёж для договора только от имени владельца объекта."""
		from app.services.contract_service import ContractService

		contract, prop_owner_id = await ContractService.get_with_access(payload.contract_id, owner_id, db)
		if prop_owner_id != owner_id:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Создавать платежи может только владелец объекта")

		payment = Payment(
			contract_id=contract.id,
			amount=payload.amount,
			due_date=payload.due_date,
			status=payload.status,
			comment=payload.comment,
			payment_proof_url=payload.payment_proof_url,
			confirmation_requested_at=payload.confirmation_requested_at,
		)
		db.add(payment)
		await db.flush()
		await db.commit()
		await db.refresh(payment)
		return payment

	@staticmethod
	async def update(payment_id: int, owner_id: int, payload: PaymentUpdate, db: AsyncSession) -> Payment:
		"""Обновить платёж и сразу сохранить изменения."""

		payment = await PaymentService.get_owned(payment_id, owner_id, db)
		updates = payload.model_dump(exclude_unset=True)
		for field, value in updates.items():
			setattr(payment, field, value)

		await db.commit()
		await db.refresh(payment)
		return payment

	@staticmethod
	async def request_confirmation(payment_id: int, tenant_id: int, payload: PaymentConfirmationRequest, db: AsyncSession) -> Payment:
		"""Отправить платёж на подтверждение вместе с чеком."""
		payment, contract, _ = await PaymentService._load_payment_context(payment_id, db)

		if contract.tenant_id != tenant_id:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Запрос подтверждения доступен только арендатору")

		if payment.status not in {"pending", "overdue"}:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Подтверждение можно запросить только для ожидающего платежа")

		payment.payment_proof_url = payload.payment_proof_url
		payment.comment = payload.comment
		payment.confirmation_requested_at = datetime.now(timezone.utc)
		await PaymentService._apply_status(payment, "waiting_confirmation", db)
		await db.commit()
		await db.refresh(payment)
		return payment

	@staticmethod
	async def confirm_payment(payment_id: int, owner_id: int, db: AsyncSession) -> Payment:
		"""Подтвердить оплату после проверки чека."""
		payment, _, prop_owner_id = await PaymentService._load_payment_context(payment_id, db)

		if prop_owner_id != owner_id:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Подтверждать оплату может только владелец объекта")

		if payment.status != "waiting_confirmation":
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Подтвердить можно только платеж в статусе ожидания подтверждения")

		await PaymentService._apply_status(payment, "paid", db)
		await db.commit()
		await db.refresh(payment)
		return payment

	@staticmethod
	async def reject_confirmation(payment_id: int, owner_id: int, db: AsyncSession) -> Payment:
		"""Отклонить подтверждение и вернуть платёж в ожидаемое состояние."""
		payment, _, prop_owner_id = await PaymentService._load_payment_context(payment_id, db)

		if prop_owner_id != owner_id:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Отклонять подтверждение может только владелец объекта")

		if payment.status != "waiting_confirmation":
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Отклонить можно только платеж в статусе ожидания подтверждения")

		payment.confirmation_requested_at = None
		payment.status = "overdue" if payment.due_date < date.today() else "pending"
		await db.flush()
		await db.commit()
		await db.refresh(payment)
		return payment

	@staticmethod
	async def delete(payment_id: int, owner_id: int, db: AsyncSession) -> None:
		"""Удалить платёж и сохранить удаление."""
		payment = await PaymentService.get_owned(payment_id, owner_id, db)
		await db.delete(payment)
		await db.commit()

	@staticmethod
	async def get_with_access(payment_id: int, user_id: int, db: AsyncSession) -> tuple[Payment, int]:
		"""Получить платёж и проверить доступ (владелец или арендатор).

		Returns:
			tuple[Payment, owner_id]: платёж и ID владельца объекта
		"""
		payment, contract, owner_id = await PaymentService._load_payment_context(payment_id, db)

		if user_id not in (contract.tenant_id, owner_id):
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа к этому платежу")

		return payment, owner_id

	@staticmethod
	async def get_owned(payment_id: int, owner_id: int, db: AsyncSession) -> Payment:
		"""Получить платёж только для владельца объекта."""
		payment, prop_owner_id = await PaymentService.get_with_access(payment_id, owner_id, db)
		if prop_owner_id != owner_id:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Только владелец может изменять платежи")
		return payment
