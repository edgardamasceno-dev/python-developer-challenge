from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from fastapi import Depends
from src.core.config import get_settings
from src.repositories.vehicle import VehicleRepository
from src.services.vehicle import VehicleService
from src.services.cache import CacheService
from src.services.health import HealthService

settings = get_settings()

engine_options = {}
if not settings.database_url.startswith("sqlite"):
    engine_options.update(
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_max_overflow
    )

engine = create_async_engine(
    settings.database_url,
    **engine_options
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

cache_service = CacheService()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_cache() -> CacheService:
    return cache_service


async def get_vehicle_service(
    db: AsyncSession = Depends(get_db),
    cache: CacheService = Depends(get_cache)
) -> VehicleService:
    repository = VehicleRepository(db)
    return VehicleService(repository, cache)


async def get_health_service(
    db: AsyncSession = Depends(get_db),
    cache: CacheService = Depends(get_cache)
) -> HealthService:
    return HealthService(db, cache)