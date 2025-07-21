from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal


class VehicleFilter(BaseModel):
    search_text: Optional[str] = Field(None, description="Full-text search query")
    brand: Optional[str] = None
    model: Optional[str] = None
    year_min: Optional[int] = None
    year_max: Optional[int] = None
    price_min: Optional[Decimal] = None
    price_max: Optional[Decimal] = None
    mileage_min: Optional[int] = Field(None, alias="km_min")
    mileage_max: Optional[int] = Field(None, alias="km_max")
    fuel_type: Optional[str] = None
    color: Optional[str] = None
    doors: Optional[int] = None
    transmission: Optional[str] = None
    cursor: Optional[str] = Field(None, description="Pagination cursor (last vehicle UUID)")
    sort_by: Optional[str] = Field("id", description="Sort field: id, price, year, mileage")
    sort_order: Optional[str] = Field("asc", description="Sort order: asc or desc")


class VehicleResponse(BaseModel):
    id: str
    brand: str
    model: str
    manufacture_year: int
    model_year: int
    engine_size: float
    fuel_type: str
    color: str
    mileage: int
    doors: int
    transmission: str
    price: float
    
    model_config = {
        'protected_namespaces': ()
    }


class VehicleSearchResult(BaseModel):
    vehicles: List[VehicleResponse]
    total_count: int
    has_more: bool
    next_cursor: Optional[str]


class BrandListResponse(BaseModel):
    brands: List[str]


class ModelListResponse(BaseModel):
    models: List[str]


class YearRangeResponse(BaseModel):
    min_year: int
    max_year: int


class PriceRangeResponse(BaseModel):
    min_price: float
    max_price: float


class MileageRangeResponse(BaseModel):
    min_mileage: int
    max_mileage: int


class ColorListResponse(BaseModel):
    colors: List[str]


class FuelTypeListResponse(BaseModel):
    fuel_types: List[str]


class TransmissionListResponse(BaseModel):
    transmissions: List[str]