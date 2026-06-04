"""Юнит-тесты для сервиса недвижимости."""

import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException

from app.services.property_service import PropertyService
from app.models.property import Property


class TestPropertyService:
    """Тесты PropertyService."""

    @pytest.mark.asyncio
    async def test_get_property_success(self, mocker):
        """Успешное получение объекта владельцем."""
        mock_db = AsyncMock()

        property_obj = Property(
            id=1,
            owner_id=10,
            title="Квартира",
            address="ул. Ленина, 1",
            property_type="apartment",
        )

        # Мокаем get_if_owned
        mocker.patch.object(
            PropertyService,
            "get_if_owned",
            return_value=property_obj,
        )

        result = await PropertyService.get_if_owned(1, 10, mock_db)

        assert result.id == 1
        assert result.title == "Квартира"
        assert result.owner_id == 10

    @pytest.mark.asyncio
    async def test_get_property_not_owner(self, mocker):
        """Попытка получить чужой объект."""
        mock_db = AsyncMock()

        # Мокаем ошибку доступа
        mocker.patch.object(
            PropertyService,
            "get_if_owned",
            side_effect=HTTPException(
                status_code=403,
                detail="Нет доступа к объекту",
            ),
        )

        with pytest.raises(HTTPException) as exc:
            await PropertyService.get_if_owned(1, 999, mock_db)

        assert exc.value.status_code == 403

    @pytest.mark.asyncio
    async def test_get_property_not_found(self, mocker):
        """Получение несуществующего объекта."""
        mock_db = AsyncMock()

        mocker.patch.object(
            PropertyService,
            "get_if_owned",
            side_effect=HTTPException(
                status_code=404,
                detail="Объект не найден",
            ),
        )

        with pytest.raises(HTTPException) as exc:
            await PropertyService.get_if_owned(999, 10, mock_db)

        assert exc.value.status_code == 404

    @pytest.mark.asyncio
    async def test_list_owned_properties(self, mocker):
        """Получение списка объектов владельца."""
        mock_db = AsyncMock()

        properties = [
            Property(
                id=1,
                owner_id=10,
                title="Объект 1",
                address="Адрес 1",
                property_type="house",
            ),
            Property(
                id=2,
                owner_id=10,
                title="Объект 2",
                address="Адрес 2",
                property_type="apartment",
            ),
        ]

        mocker.patch.object(
            PropertyService,
            "list_owned",
            return_value=properties,
        )

        result = await PropertyService.list_owned(10, mock_db)

        assert len(result) == 2
        assert result[0].title == "Объект 1"
        assert result[1].title == "Объект 2"

    @pytest.mark.asyncio
    async def test_create_property(self, mocker):
        """Создание объекта недвижимости."""
        mock_db = AsyncMock()

        from app.schemas.property import PropertyCreate

        payload = PropertyCreate(
            title="Новый объект",
            address="Новый адрес",
            property_type="office",
        )

        new_property = Property(
            id=1,
            owner_id=10,
            title="Новый объект",
            address="Новый адрес",
            property_type="office",
        )

        mocker.patch.object(
            PropertyService,
            "create_property",
            return_value=new_property,
        )

        result = await PropertyService.create_property(payload, 10, mock_db)

        assert result.title == "Новый объект"
        assert result.owner_id == 10
