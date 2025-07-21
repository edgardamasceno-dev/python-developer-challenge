import pytest
from unittest.mock import AsyncMock, MagicMock
from src.services.health import HealthService
from src.services.cache import CacheService
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_health_check_all_healthy():
    mock_session = AsyncMock(spec=AsyncSession)
    mock_cache = MagicMock(spec=CacheService)
    mock_cache.cache = {}  
    
    mock_session.execute = AsyncMock(return_value=MagicMock())
    
    health_service = HealthService(mock_session, mock_cache)
    
    health_service.vehicle_repository.check_table_exists = AsyncMock(return_value=True)
    
    status = await health_service.get_health_status()
    
    assert status["status"] == "healthy"
    assert status["checks"]["database_connection"] is True
    assert status["checks"]["vehicles_table"] is True
    assert status["checks"]["cache_available"] is True


@pytest.mark.asyncio
async def test_health_check_database_failure():
    mock_session = AsyncMock(spec=AsyncSession)
    mock_cache = MagicMock(spec=CacheService)
    mock_cache.cache = {}
    
    mock_session.execute = AsyncMock(side_effect=Exception("Connection failed"))
    
    health_service = HealthService(mock_session, mock_cache)
    
    status = await health_service.get_health_status()
    
    assert status["status"] == "unhealthy"
    assert status["checks"]["database_connection"] is False
    assert status["checks"]["vehicles_table"] is False  
    assert status["checks"]["cache_available"] is True


@pytest.mark.asyncio
async def test_health_check_table_missing():
    mock_session = AsyncMock(spec=AsyncSession)
    mock_cache = MagicMock(spec=CacheService)
    mock_cache.cache = {}
    
    mock_session.execute = AsyncMock(return_value=MagicMock())
    
    health_service = HealthService(mock_session, mock_cache)
    
    health_service.vehicle_repository.check_table_exists = AsyncMock(return_value=False)
    
    status = await health_service.get_health_status()
    
    assert status["status"] == "unhealthy"
    assert status["checks"]["database_connection"] is True
    assert status["checks"]["vehicles_table"] is False
    assert status["checks"]["cache_available"] is True


@pytest.mark.asyncio
async def test_check_cache_status():
    mock_session = AsyncMock(spec=AsyncSession)
    mock_cache_with_attr = MagicMock(spec=CacheService)
    mock_cache_with_attr.cache = {}
    
    health_service = HealthService(mock_session, mock_cache_with_attr)
    
    assert await health_service.check_cache_status() is True
    
    mock_cache_without_attr = MagicMock(spec=CacheService)
    del mock_cache_without_attr.cache
    
    health_service.cache = mock_cache_without_attr
    assert await health_service.check_cache_status() is False