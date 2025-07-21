from sqlalchemy import select, func, text, cast, String
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Tuple
from uuid import UUID
from src.models.database import Vehicle
from src.models.schemas import VehicleFilter
from src.repositories.base import BaseRepository


class VehicleRepository(BaseRepository[Vehicle]):
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, Vehicle)
    
    async def search_vehicles(self, filters: VehicleFilter) -> Tuple[List[Vehicle], int]:
        base_query = select(Vehicle)
        
        if filters.search_text:
            search_terms = filters.search_text.lower().split()
            tsquery_parts = [f"{term}:*" for term in search_terms]
            tsquery = " & ".join(tsquery_parts)
            
            base_query = base_query.where(
                Vehicle.search_vector.match(tsquery, postgresql_regconfig='portuguese')
            )
        
        if filters.brand:
            base_query = base_query.where(Vehicle.brand == filters.brand)
        if filters.model:
            base_query = base_query.where(Vehicle.model == filters.model)
        if filters.year_min:
            base_query = base_query.where(Vehicle.manufacture_year >= filters.year_min)
        if filters.year_max:
            base_query = base_query.where(Vehicle.manufacture_year <= filters.year_max)
        if filters.price_min:
            base_query = base_query.where(Vehicle.price >= filters.price_min)
        if filters.price_max:
            base_query = base_query.where(Vehicle.price <= filters.price_max)
        if filters.mileage_min:
            base_query = base_query.where(Vehicle.mileage >= filters.mileage_min)
        if filters.mileage_max:
            base_query = base_query.where(Vehicle.mileage <= filters.mileage_max)
        if filters.fuel_type:
            base_query = base_query.where(Vehicle.fuel_type == filters.fuel_type)
        if filters.color:
            base_query = base_query.where(
                func.lower(Vehicle.color).like(f"%{filters.color.lower()}%")
            )
        if filters.doors:
            base_query = base_query.where(Vehicle.doors == filters.doors)
        if filters.transmission:
            base_query = base_query.where(Vehicle.transmission == filters.transmission)
        
        count_query = select(func.count()).select_from(base_query.subquery())
        total_count = await self.session.scalar(count_query)
        
        if filters.sort_by == "price":
            order_field = Vehicle.price
        elif filters.sort_by == "year":
            order_field = Vehicle.model_year
        elif filters.sort_by == "mileage":
            order_field = Vehicle.mileage
        else:
            order_field = Vehicle.id  
        
        if filters.sort_order == "desc":
            base_query = base_query.order_by(order_field.desc(), Vehicle.id.desc())
        else:
            base_query = base_query.order_by(order_field.asc(), Vehicle.id.asc())
        
        if filters.cursor:
            try:
                cursor_uuid = UUID(filters.cursor)
                if filters.sort_order == "desc":
                    base_query = base_query.where(Vehicle.id < cursor_uuid)
                else:
                    base_query = base_query.where(Vehicle.id > cursor_uuid)
            except ValueError:
                pass
        
        base_query = base_query.limit(10)
        
        result = await self.session.execute(base_query)
        vehicles = result.scalars().all()
        
        return vehicles, total_count
    
    async def get_unique_brands(self) -> List[str]:
        query = select(Vehicle.brand).distinct().order_by(Vehicle.brand)
        result = await self.session.execute(query)
        return [row[0] for row in result]
    
    async def get_unique_models(self, brands: Optional[List[str]] = None) -> List[str]:
        query = select(Vehicle.model).distinct()
        if brands:
            query = query.where(Vehicle.brand.in_(brands))
        query = query.order_by(Vehicle.model)
        
        result = await self.session.execute(query)
        return [row[0] for row in result]
    
    async def get_year_range(self) -> Tuple[int, int]:
        query = select(
            func.min(Vehicle.manufacture_year),
            func.max(Vehicle.manufacture_year)
        )
        result = await self.session.execute(query)
        row = result.one()
        return row[0] or 0, row[1] or 0
    
    async def get_price_range(self) -> Tuple[float, float]:
        query = select(
            func.min(Vehicle.price),
            func.max(Vehicle.price)
        )
        result = await self.session.execute(query)
        row = result.one()
        return float(row[0] or 0), float(row[1] or 0)
    
    async def get_mileage_range(self) -> Tuple[int, int]:
        query = select(
            func.min(Vehicle.mileage),
            func.max(Vehicle.mileage)
        )
        result = await self.session.execute(query)
        row = result.one()
        return row[0] or 0, row[1] or 0
    
    async def get_unique_colors(self) -> List[str]:
        query = select(Vehicle.color).distinct().order_by(Vehicle.color)
        result = await self.session.execute(query)
        return [row[0] for row in result]
    
    async def get_unique_fuel_types(self) -> List[str]:
        query = select(Vehicle.fuel_type).distinct().order_by(Vehicle.fuel_type)
        result = await self.session.execute(query)
        return [row[0] for row in result]
    
    async def get_unique_transmissions(self) -> List[str]:
        query = select(Vehicle.transmission).distinct().order_by(Vehicle.transmission)
        result = await self.session.execute(query)
        return [row[0] for row in result]
    
    async def check_table_exists(self) -> bool:
        if self.session.bind.dialect.name == 'postgresql':
            query = text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'vehicles'
                );
            """)
        else:
            query = text("SELECT name FROM sqlite_master WHERE type='table' AND name='vehicles'")
        result = await self.session.execute(query)
        return result.scalar()