"""Сервис для работы с договорами и генерации платежей."""
import calendar
from datetime import date
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.contract import Contract
from app.models.property import Property
from app.models.user import User
from app.schemas.contract import ContractCreate, ContractCreateByEmail, ContractUpdate
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
        """Создать договор и автоматически сгенерировать платежи.

        Процесс:
        1. Проверяем что объект существует и принадлежит владельцу
        2. Проверяем что арендатор существует
        3. Создаём запись договора в БД
        4. Генерируем платежи на каждый месяц (автоматически!)
        5. Возвращаем договор с привязанными платежами
        """
        # Проверяем объект
        prop_stmt = select(Property).where(Property.id == payload.property_id)
        prop_res = await db.execute(prop_stmt)
        prop = prop_res.scalars().first()

        if prop is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объект не найден")

        if prop.owner_id != owner_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Создавать договор может только владелец объекта")

        # Проверяем арендатора
        tenant_stmt = select(User).where(User.id == payload.tenant_id)
        tenant_res = await db.execute(tenant_stmt)
        tenant = tenant_res.scalars().first()
        if tenant is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Арендатор не найден")

        # Создаём договор
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
        await db.flush()  # получаем contract_obj.id перед генерацией платежей

        # Автоматически генерируем платежи на все месяцы договора
        await PaymentService.generate_payments_for_contract(contract_obj, db)
        await db.commit()
        await db.refresh(contract_obj)

        return contract_obj

    @staticmethod
    async def create_contract_by_email(payload: ContractCreateByEmail, owner_user: User, db: AsyncSession) -> Contract:
        """Создать договор по email арендатора."""
        prop_stmt = select(Property).where(Property.id == payload.property_id)
        prop_res = await db.execute(prop_stmt)
        prop = prop_res.scalars().first()

        if prop is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объект не найден")

        if prop.owner_id != owner_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Создавать договор может только владелец объекта")

        tenant_stmt = select(User).where(User.email == payload.tenant_email)
        tenant_res = await db.execute(tenant_stmt)
        tenant = tenant_res.scalars().first()

        if tenant is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Арендатор не найден")

        contract_obj = Contract(
            property_id=payload.property_id,
            tenant_id=tenant.id,
            start_date=payload.start_date,
            end_date=payload.end_date,
            monthly_payment=payload.monthly_payment,
            security_deposit=payload.security_deposit,
            status="pending_tenant_confirmation",
        )

        db.add(contract_obj)
        await db.commit()
        await db.refresh(contract_obj)

        return contract_obj

    @staticmethod
    async def list_related_contracts(user_id: int, db: AsyncSession) -> List[Contract]:
        """Получить все договоры, где пользователь связан как арендатор или владелец."""
        stmt = (
            select(Contract)
            .join(Property)
            .where(or_(Contract.tenant_id == user_id, Property.owner_id == user_id))
            .order_by(Contract.created_at.desc())
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def list_owner_contracts(owner_id: int, db: AsyncSession) -> List[Contract]:
        """Получить все договоры по объектам владельца."""
        stmt = select(Contract).join(Property).where(Property.owner_id == owner_id).order_by(Contract.created_at.desc())
        result = await db.execute(stmt)
        return list(result.scalars().all())

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

    @staticmethod
    async def list_tenant_contracts(tenant_id: int, db: AsyncSession) -> List[Contract]:
        """Получить все договоры арендатора."""
        stmt = (
            select(Contract)
            .where(Contract.tenant_id == tenant_id)
            .options(selectinload(Contract.property).selectinload(Property.owner))
            .order_by(Contract.created_at.desc())
        )
        result = await db.execute(stmt)
        return list(result.scalars().unique().all())

    @staticmethod
    async def confirm_contract(contract_id: int, tenant_id: int, db: AsyncSession) -> Contract:
        """Подтвердить договор арендатором и сгенерировать платежи."""
        stmt = select(Contract).where(
            Contract.id == contract_id,
            Contract.tenant_id == tenant_id,
            Contract.status == "pending_tenant_confirmation",
        )
        res = await db.execute(stmt)
        contract = res.scalars().first()

        if contract is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Договор не найден или не требует подтверждения")

        contract.status = "active"
        await db.flush()

        await PaymentService.generate_payments_for_contract(contract, db)
        await db.commit()
        await db.refresh(contract)

        return contract

    @staticmethod
    async def update(contract_id: int, owner_id: int, payload: ContractUpdate, db: AsyncSession) -> Contract:
        """Обновить договор и сразу сохранить изменения."""
        contract = await ContractService.get_owned(contract_id, owner_id, db)
        updates = payload.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(contract, field, value)
        await db.commit()
        await db.refresh(contract)
        return contract

    @staticmethod
    async def delete(contract_id: int, owner_id: int, db: AsyncSession) -> None:
        """Удалить договор и сохранить удаление."""
        contract = await ContractService.get_owned(contract_id, owner_id, db)
        await db.delete(contract)
        await db.commit()
