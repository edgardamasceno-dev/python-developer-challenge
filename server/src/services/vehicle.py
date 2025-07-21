from typing import List, Tuple, Optional
from src.repositories.vehicle import VehicleRepository
from src.services.cache import CacheService
from src.models.schemas import (
    VehicleFilter,
    VehicleResponse,
    VehicleSearchResult,
    BrandListResponse,
    ModelListResponse,
    YearRangeResponse,
    PriceRangeResponse,
    MileageRangeResponse,
    ColorListResponse,
    FuelTypeListResponse,
    TransmissionListResponse
)
from src.models.database import Vehicle
import structlog

logger = structlog.get_logger()


class VehicleService:
    
    def __init__(self, repository: VehicleRepository, cache: CacheService):
        self.repository = repository
        self.cache = cache
    
    async def search_vehicles(self, filters: VehicleFilter) -> VehicleSearchResult:
        vehicles, total_count = await self.repository.search_vehicles(filters)
        
        vehicle_responses = [
            VehicleResponse(
                id=str(vehicle.id),
                brand=vehicle.brand,
                model=vehicle.model,
                manufacture_year=vehicle.manufacture_year,
                model_year=vehicle.model_year,
                engine_size=vehicle.engine_size,
                fuel_type=vehicle.fuel_type,
                color=vehicle.color,
                mileage=vehicle.mileage,
                doors=vehicle.doors,
                transmission=vehicle.transmission,
                price=float(vehicle.price)
            )
            for vehicle in vehicles
        ]
        
        has_more = len(vehicles) == 10
        next_cursor = str(vehicles[-1].id) if has_more and vehicles else None
        
        return VehicleSearchResult(
            vehicles=vehicle_responses,
            total_count=total_count,
            has_more=has_more,
            next_cursor=next_cursor
        )
    
    async def get_brands(self) -> BrandListResponse:
        cache_key = self.cache.generate_key("brands")
        
        async def fetch_brands():
            brands = await self.repository.get_unique_brands()
            return {"brands": brands}
        
        result = await self.cache.get_or_set(cache_key, fetch_brands)
        return BrandListResponse(**result)
    
    async def get_models(self, brands: Optional[List[str]] = None) -> ModelListResponse:
        cache_key = self.cache.generate_key("models", brands=brands)
        
        async def fetch_models():
            models = await self.repository.get_unique_models(brands)
            return {"models": models}
        
        result = await self.cache.get_or_set(cache_key, fetch_models)
        return ModelListResponse(**result)
    
    async def get_year_range(self) -> YearRangeResponse:
        cache_key = self.cache.generate_key("year_range")
        
        async def fetch_year_range():
            min_year, max_year = await self.repository.get_year_range()
            return {"min_year": min_year, "max_year": max_year}
        
        result = await self.cache.get_or_set(cache_key, fetch_year_range)
        return YearRangeResponse(**result)
    
    async def get_price_range(self) -> PriceRangeResponse:
        cache_key = self.cache.generate_key("price_range")
        
        async def fetch_price_range():
            min_price, max_price = await self.repository.get_price_range()
            return {"min_price": min_price, "max_price": max_price}
        
        result = await self.cache.get_or_set(cache_key, fetch_price_range)
        return PriceRangeResponse(**result)
    
    async def get_mileage_range(self) -> MileageRangeResponse:
        cache_key = self.cache.generate_key("mileage_range")
        
        async def fetch_mileage_range():
            min_mileage, max_mileage = await self.repository.get_mileage_range()
            return {"min_mileage": min_mileage, "max_mileage": max_mileage}
        
        result = await self.cache.get_or_set(cache_key, fetch_mileage_range)
        return MileageRangeResponse(**result)
    
    async def get_colors(self) -> ColorListResponse:
        cache_key = self.cache.generate_key("colors")
        
        async def fetch_colors():
            colors = await self.repository.get_unique_colors()
            return {"colors": colors}
        
        result = await self.cache.get_or_set(cache_key, fetch_colors)
        return ColorListResponse(**result)
    
    async def get_fuel_types(self) -> FuelTypeListResponse:
        cache_key = self.cache.generate_key("fuel_types")
        
        async def fetch_fuel_types():
            fuel_types = await self.repository.get_unique_fuel_types()
            return {"fuel_types": fuel_types}
        
        result = await self.cache.get_or_set(cache_key, fetch_fuel_types)
        return FuelTypeListResponse(**result)
    
    async def get_transmissions(self) -> TransmissionListResponse:
        cache_key = self.cache.generate_key("transmissions")
        
        async def fetch_transmissions():
            transmissions = await self.repository.get_unique_transmissions()
            return {"transmissions": transmissions}
        
        result = await self.cache.get_or_set(cache_key, fetch_transmissions)
        return TransmissionListResponse(**result)
    
    async def check_health(self) -> bool:
        return await self.repository.check_table_exists()