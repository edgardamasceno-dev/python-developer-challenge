from typing import List, Optional, Dict, Any, Union
from src.services.vehicle import VehicleService
from src.models.schemas import VehicleFilter, VehicleSearchResult
import structlog

logger = structlog.get_logger()


class VehicleMCPTools:
    
    def __init__(self, vehicle_service: VehicleService):
        self.vehicle_service = vehicle_service
    
    async def search_vehicles(
        self,
        search_text: Optional[str] = None,
        brand: Optional[str] = None,
        model: Optional[str] = None,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        mileage_min: Optional[int] = None,
        mileage_max: Optional[int] = None,
        fuel_type: Optional[str] = None,
        color: Optional[str] = None,
        doors: Optional[int] = None,
        transmission: Optional[str] = None,
        cursor: Optional[str] = None,
        sort_by: Optional[str] = "id",
        sort_order: Optional[str] = "asc"
    ) -> Dict[str, Any]:
        filters = VehicleFilter(
            search_text=search_text,
            brand=brand,
            model=model,
            year_min=year_min,
            year_max=year_max,
            price_min=price_min,
            price_max=price_max,
            km_min=mileage_min,  
            km_max=mileage_max,  
            fuel_type=fuel_type,
            color=color,
            doors=doors,
            transmission=transmission,
            cursor=cursor,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        result = await self.vehicle_service.search_vehicles(filters)
        return result.model_dump()
    
    async def list_brands(self) -> Dict[str, Any]:
        result = await self.vehicle_service.get_brands()
        return result.model_dump()
    
    async def list_models(self, brand: Optional[Union[str, List[str]]] = None) -> Dict[str, Any]:
        brands_list = None
        if brand is not None:
            if isinstance(brand, list):
                brands_list = brand
            else:
                brands_list = [brand]
            
        result = await self.vehicle_service.get_models(brands_list)
        return result.model_dump()
    
    async def get_year_range(self) -> Dict[str, Any]:
        result = await self.vehicle_service.get_year_range()
        return result.model_dump()
    
    async def get_price_range(self) -> Dict[str, Any]:
        result = await self.vehicle_service.get_price_range()
        return result.model_dump()
    
    async def get_mileage_range(self) -> Dict[str, Any]:
        result = await self.vehicle_service.get_mileage_range()
        return result.model_dump()
    
    async def list_available_colors(self) -> Dict[str, Any]:
        result = await self.vehicle_service.get_colors()
        return result.model_dump()
    
    async def list_fuel_types(self) -> Dict[str, Any]:
        result = await self.vehicle_service.get_fuel_types()
        return result.model_dump()
    
    async def list_transmissions(self) -> Dict[str, Any]:
        result = await self.vehicle_service.get_transmissions()
        return result.model_dump()