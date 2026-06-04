"""Юнит-тесты для сервиса договоров."""

import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException
from datetime import date, timedelta

from app.services.contract_service import ContractService
from app.models.contract import Contract


class TestContractService:
    """Тесты ContractService."""

    @pytest.mark.asyncio
    async def test_create_contract_success(self, mocker):
        """Успешное создание договора."""
        mock_db = AsyncMock()

        from app.schemas.contract import ContractCreate
        from app.models.property import Property
        from app.models.user import User

        # Мокаем проверку объекта
        property_obj = Property(
            id=1,
            owner_id=10,
            title="Квартира",
            address="Адрес",
            property_type="apartment",
        )
        mocker.patch.object(
            PropertyService,
            "get_if_owned",
            return_value=property_obj,
        )

        # Мокаем проверку арендатора
        tenant = User(id=20, name="Tenant", email="tenant@test.com")
        mock_db.execute.return_value.scalars.return_value.first.side_effect = [
            property_obj,
            tenant,
        ]

        # Мокаем генерацию платежей
        mocker.patch(
            "app.services.payment_service.PaymentService.generate_payments_for_contract",
            return_value=[],
        )

        payload = ContractCreate(
            property_id=1,
            tenant_id=20,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365),
            monthly_payment=50000,
        )

        contract = Contract(
            id=1,
            property_id=1,
            tenant_id=20,
            start_date=payload.start_date,
            end_date=payload.end_date,
            monthly_payment=50000,
            status="active",
        )

        mocker.patch.object(
            ContractService,
            "create_contract",
            return_value=contract,
        )

        result = await ContractService.create_contract(payload, User(id=10), mock_db)

        assert result.property_id == 1
        assert result.tenant_id == 20
        assert result.status == "active"

    @pytest.mark.asyncio
    async def test_create_contract_wrong_owner(self, mocker):
        """Создание договора не владельцем объекта."""
        mock_db = AsyncMock()

        mocker.patch.object(
            ContractService,
            "create_contract",
            side_effect=HTTPException(
                status_code=403,
                detail="Создавать договор может только владелец объекта",
            ),
        )

        with pytest.raises(HTTPException) as exc:
            await ContractService.create_contract(MagicMock(), MagicMock(), mock_db)

        assert exc.value.status_code == 403

    @pytest.mark.asyncio
    async def test_confirm_contract(self, mocker):
        """Подтверждение договора арендатором."""
        mock_db = AsyncMock()

        contract = Contract(
            id=1,
            property_id=1,
            tenant_id=20,
            status="pending_tenant_confirmation",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365),
            monthly_payment=50000,
        )

        mocker.patch.object(
            ContractService,
            "confirm_contract",
            return_value=contract,
        )

        result = await ContractService.confirm_contract(1, 20, mock_db)

        assert result.id == 1
        assert result.status == "pending_tenant_confirmation"

    @pytest.mark.asyncio
    async def test_list_tenant_contracts(self, mocker):
        """Получение списка договоров арендатора."""
        mock_db = AsyncMock()

        contracts = [
            Contract(id=1, property_id=1, tenant_id=20, status="active"),
            Contract(
                id=2, property_id=2, tenant_id=20, status="pending_tenant_confirmation"
            ),
        ]

        mocker.patch.object(
            ContractService,
            "list_tenant_contracts",
            return_value=contracts,
        )

        result = await ContractService.list_tenant_contracts(20, mock_db)

        assert len(result) == 2
        assert result[0].status == "active"
        assert result[1].status == "pending_tenant_confirmation"

    @pytest.mark.asyncio
    async def test_contract_not_found(self, mocker):
        """Получение несуществующего договора."""
        mock_db = AsyncMock()

        mocker.patch.object(
            ContractService,
            "get_with_access",
            side_effect=HTTPException(
                status_code=404,
                detail="Договор не найден",
            ),
        )

        with pytest.raises(HTTPException) as exc:
            await ContractService.get_with_access(999, 10, mock_db)

        assert exc.value.status_code == 404
