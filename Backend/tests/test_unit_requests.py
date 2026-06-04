"""Юнит-тесты для сервиса заявок."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException

from app.services.request_service import RequestService
from app.models.request import Request as MaintenanceRequest


class TestRequestService:
    """Тесты RequestService."""

    @pytest.mark.asyncio
    async def test_create_request_success(self, mocker):
        """Успешное создание заявки."""
        mock_db = AsyncMock()

        req = MaintenanceRequest(
            id=1,
            contract_id=5,
            title="Протечка",
            message="Течёт кран в ванной",
            status="open",
        )

        mocker.patch.object(
            RequestService,
            "create_request",
            return_value=req,
        )

        from app.schemas.request import RequestCreate

        payload = RequestCreate(
            contract_id=5,
            title="Протечка",
            message="Течёт кран в ванной",
        )

        result = await RequestService.create_request(payload, 20, mock_db)

        assert result.title == "Протечка"
        assert result.status == "open"
        assert result.contract_id == 5

    @pytest.mark.asyncio
    async def test_create_request_no_active_contract(self, mocker):
        """Создание заявки без активного договора."""
        mock_db = AsyncMock()

        mocker.patch.object(
            RequestService,
            "create_request",
            side_effect=HTTPException(
                status_code=404,
                detail="Активный договор не найден",
            ),
        )

        with pytest.raises(HTTPException) as exc:
            await RequestService.create_request(MagicMock(), 20, mock_db)

        assert exc.value.status_code == 404

    @pytest.mark.asyncio
    async def test_update_request_status(self, mocker):
        """Изменение статуса заявки владельцем."""
        mock_db = AsyncMock()

        updated_req = MaintenanceRequest(
            id=1,
            contract_id=5,
            title="Протечка",
            message="Течёт кран",
            status="completed",
        )

        mocker.patch.object(
            RequestService,
            "update_request",
            return_value=updated_req,
        )

        from app.schemas.request import RequestUpdate

        payload = RequestUpdate(status="completed")

        result = await RequestService.update_request(1, 10, mock_db, payload)

        assert result.status == "completed"

    @pytest.mark.asyncio
    async def test_update_request_unauthorized(self, mocker):
        """Изменение заявки не владельцем."""
        mock_db = AsyncMock()

        mocker.patch.object(
            RequestService,
            "update_request",
            side_effect=HTTPException(
                status_code=403,
                detail="Только владелец может изменять заявки",
            ),
        )

        with pytest.raises(HTTPException) as exc:
            await RequestService.update_request(1, 999, mock_db, MagicMock())

        assert exc.value.status_code == 403

    @pytest.mark.asyncio
    async def test_list_owner_requests(self, mocker):
        """Получение заявок владельца."""
        mock_db = AsyncMock()

        requests = [
            MaintenanceRequest(
                id=1, contract_id=5, title="Заявка 1", message="...", status="open"
            ),
            MaintenanceRequest(
                id=2, contract_id=6, title="Заявка 2", message="...", status="completed"
            ),
        ]

        mocker.patch.object(
            RequestService,
            "list_owner_requests",
            return_value=requests,
        )

        result = await RequestService.list_owner_requests(10, mock_db)

        assert len(result) == 2
        assert result[0].status == "open"
        assert result[1].status == "completed"

    @pytest.mark.asyncio
    async def test_list_tenant_requests(self, mocker):
        """Получение заявок арендатора."""
        mock_db = AsyncMock()

        requests = [
            MaintenanceRequest(
                id=1,
                contract_id=5,
                title="Заявка 1",
                message="...",
                status="in_progress",
            ),
        ]

        mocker.patch.object(
            RequestService,
            "list_tenant_requests",
            return_value=requests,
        )

        result = await RequestService.list_tenant_requests(20, mock_db)

        assert len(result) == 1
        assert result[0].status == "in_progress"
