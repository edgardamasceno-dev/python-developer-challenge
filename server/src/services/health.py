from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.services.cache import CacheService
from src.repositories.vehicle import VehicleRepository
import structlog

logger = structlog.get_logger()


class HealthService:
    
    def __init__(self, session: AsyncSession, cache: CacheService):
        self.session = session
        self.cache = cache
        self.vehicle_repository = VehicleRepository(session)
    
    async def check_database_connection(self) -> bool:
        try:
            await self.session.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error("Database connection failed", error=str(e))
            return False
    
    async def check_vehicles_table(self) -> bool:
        try:
            return await self.vehicle_repository.check_table_exists()
        except Exception as e:
            logger.error("Failed to check vehicles table", error=str(e))
            return False
    
    async def check_cache_status(self) -> bool:
        try:
            return hasattr(self.cache, 'cache')
        except Exception as e:
            logger.error("Cache check failed", error=str(e))
            return False
    
    async def get_health_status(self) -> dict:
        database_ok = await self.check_database_connection()
        table_ok = await self.check_vehicles_table() if database_ok else False
        cache_ok = await self.check_cache_status()
        
        all_ok = database_ok and table_ok and cache_ok
        
        return {
            "status": "healthy" if all_ok else "unhealthy",
            "checks": {
                "database_connection": database_ok,
                "vehicles_table": table_ok,
                "cache_available": cache_ok
            }
        }