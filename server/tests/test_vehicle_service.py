import pytest
from unittest.mock import AsyncMock, MagicMock
from src.services.vehicle import VehicleService
from src.services.cache import CacheService
from src.repositories.vehicle import VehicleRepository
from src.models.schemas import VehicleFilter
from src.models.database import Vehicle
from uuid import uuid4
from decimal import Decimal
from datetime import datetime


@pytest.mark.asyncio
async def test_search_vehicles_no_cache(test_cache):
    mock_repo = AsyncMock(spec=VehicleRepository)
    sample_vehicle = MagicMock(spec=Vehicle)
    sample_vehicle.id = uuid4()
    sample_vehicle.brand = "Toyota"
    sample_vehicle.model = "Corolla"
    sample_vehicle.manufacture_year = 2022
    sample_vehicle.model_year = 2023
    sample_vehicle.engine_size = 2.0
    sample_vehicle.fuel_type = "flex"
    sample_vehicle.color = "branco"
    sample_vehicle.mileage = 15000
    sample_vehicle.doors = 4
    sample_vehicle.transmission = "automatic"
    sample_vehicle.price = Decimal("95000.00")
    
    mock_repo.search_vehicles.return_value = ([sample_vehicle], 1)
    
    service = VehicleService(mock_repo, test_cache)
    
    filters = VehicleFilter(brand="Toyota")
    result = await service.search_vehicles(filters)
    
    assert result.total_count == 1
    assert len(result.vehicles) == 1
    assert result.vehicles[0].brand == "Toyota"
    assert result.has_more is False
    
    mock_repo.search_vehicles.assert_called_once()


@pytest.mark.asyncio
async def test_get_brands_with_cache(test_cache):
    mock_repo = AsyncMock(spec=VehicleRepository)
    mock_repo.get_unique_brands.return_value = ["Honda", "Toyota", "Volkswagen"]
    
    service = VehicleService(mock_repo, test_cache)
    
    result1 = await service.get_brands()
    assert result1.brands == ["Honda", "Toyota", "Volkswagen"]
    assert mock_repo.get_unique_brands.call_count == 1
    
    result2 = await service.get_brands()
    assert result2.brands == ["Honda", "Toyota", "Volkswagen"]
    assert mock_repo.get_unique_brands.call_count == 1  


@pytest.mark.asyncio
async def test_get_models_with_brand_filter(test_cache):
    mock_repo = AsyncMock(spec=VehicleRepository)
    mock_repo.get_unique_models.return_value = ["Civic", "Accord"]
    
    service = VehicleService(mock_repo, test_cache)
    
    result = await service.get_models(["Honda"])
    assert result.models == ["Civic", "Accord"]
    
    mock_repo.get_unique_models.assert_called_with(["Honda"])
    
    mock_repo.reset_mock()
    mock_repo.get_unique_models.return_value = ["Civic", "Accord", "Corolla", "Hilux"]
    result = await service.get_models(None)
    assert len(result.models) == 4
    mock_repo.get_unique_models.assert_called_with(None)


@pytest.mark.asyncio
async def test_get_year_range_cached(test_cache):
    mock_repo = AsyncMock(spec=VehicleRepository)
    mock_repo.get_year_range.return_value = (2020, 2023)
    
    service = VehicleService(mock_repo, test_cache)
    
    result1 = await service.get_year_range()
    assert result1.min_year == 2020
    assert result1.max_year == 2023
    assert mock_repo.get_year_range.call_count == 1
    
    result2 = await service.get_year_range()
    assert result2.min_year == 2020
    assert result2.max_year == 2023
    assert mock_repo.get_year_range.call_count == 1  


@pytest.mark.asyncio
async def test_get_colors_cached(test_cache):
    mock_repo = AsyncMock(spec=VehicleRepository)
    mock_repo.get_unique_colors.return_value = ["branco", "preto", "prata"]
    
    service = VehicleService(mock_repo, test_cache)
    
    result = await service.get_colors()
    assert result.colors == ["branco", "preto", "prata"]
    
    result2 = await service.get_colors()
    assert result2.colors == ["branco", "preto", "prata"]
    assert mock_repo.get_unique_colors.call_count == 1


@pytest.mark.asyncio
async def test_check_health(test_cache):
    mock_repo = AsyncMock(spec=VehicleRepository)
    mock_repo.check_table_exists.return_value = True
    
    service = VehicleService(mock_repo, test_cache)
    
    result = await service.check_health()
    assert result is True
    
    mock_repo.check_table_exists.return_value = False
    result = await service.check_health()
    assert result is False