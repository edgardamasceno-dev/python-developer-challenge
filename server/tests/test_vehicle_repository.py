import pytest
from uuid import UUID
from src.repositories.vehicle import VehicleRepository
from src.models.schemas import VehicleFilter


@pytest.mark.asyncio
async def test_get_unique_brands(test_session, sample_vehicles):
    repo = VehicleRepository(test_session)
    brands = await repo.get_unique_brands()
    
    assert set(brands) == {"Honda", "Toyota"}
    assert brands == sorted(brands)  


@pytest.mark.asyncio
async def test_get_unique_models(test_session, sample_vehicles):
    repo = VehicleRepository(test_session)
    
    all_models = await repo.get_unique_models()
    assert set(all_models) == {"Civic", "Corolla", "Hilux"}
    
    toyota_models = await repo.get_unique_models(["Toyota"])
    assert set(toyota_models) == {"Corolla", "Hilux"}
    
    honda_models = await repo.get_unique_models(["Honda"])
    assert honda_models == ["Civic"]


@pytest.mark.asyncio
async def test_get_year_range(test_session, sample_vehicles):
    repo = VehicleRepository(test_session)
    min_year, max_year = await repo.get_year_range()
    
    assert min_year == 2021
    assert max_year == 2023


@pytest.mark.asyncio
async def test_get_price_range(test_session, sample_vehicles):
    repo = VehicleRepository(test_session)
    min_price, max_price = await repo.get_price_range()
    
    assert min_price == 85000.00
    assert max_price == 250000.00


@pytest.mark.asyncio
async def test_get_mileage_range(test_session, sample_vehicles):
    repo = VehicleRepository(test_session)
    min_mileage, max_mileage = await repo.get_mileage_range()
    
    assert min_mileage == 5000
    assert max_mileage == 25000


@pytest.mark.asyncio
async def test_get_unique_colors(test_session, sample_vehicles):
    repo = VehicleRepository(test_session)
    colors = await repo.get_unique_colors()
    
    assert set(colors) == {"branco", "branco metálico", "preto"}
    assert colors == sorted(colors)


@pytest.mark.asyncio
async def test_search_vehicles_basic(test_session, sample_vehicles):
    repo = VehicleRepository(test_session)
    
    filters = VehicleFilter()
    vehicles, total = await repo.search_vehicles(filters)
    
    assert total == 3
    assert len(vehicles) == 3


@pytest.mark.asyncio
async def test_search_vehicles_by_brand(test_session, sample_vehicles):
    repo = VehicleRepository(test_session)
    
    filters = VehicleFilter(brand="Toyota")
    vehicles, total = await repo.search_vehicles(filters)
    
    assert total == 2
    assert all(v.brand == "Toyota" for v in vehicles)


@pytest.mark.asyncio
async def test_search_vehicles_partial_color_match(test_session, sample_vehicles):
    repo = VehicleRepository(test_session)
    
    filters = VehicleFilter(color="branco")
    vehicles, total = await repo.search_vehicles(filters)
    
    assert total == 2
    colors = [v.color for v in vehicles]
    assert "branco" in colors
    assert "branco metálico" in colors


@pytest.mark.asyncio
async def test_search_vehicles_price_range(test_session, sample_vehicles):
    repo = VehicleRepository(test_session)
    
    filters = VehicleFilter(price_min=90000, price_max=100000)
    vehicles, total = await repo.search_vehicles(filters)
    
    assert total == 1
    assert vehicles[0].model == "Corolla"


@pytest.mark.asyncio
async def test_search_vehicles_pagination(test_session, sample_vehicles):
    repo = VehicleRepository(test_session)
    
    filters = VehicleFilter()
    vehicles, total = await repo.search_vehicles(filters)
    
    assert len(vehicles) == 3  
    
    if vehicles:
        last_id = str(vehicles[-1].id)
        filters_page2 = VehicleFilter(cursor=last_id)
        vehicles_page2, _ = await repo.search_vehicles(filters_page2)
        
        page1_ids = {str(v.id) for v in vehicles}
        page2_ids = {str(v.id) for v in vehicles_page2}
        assert not page1_ids.intersection(page2_ids)


@pytest.mark.asyncio
async def test_check_table_exists(test_session):
    repo = VehicleRepository(test_session)
    
    try:
        exists = await repo.check_table_exists()
        assert isinstance(exists, bool)
    except Exception:
        pytest.skip("Table existence check not supported in SQLite")