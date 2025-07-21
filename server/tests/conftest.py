import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from httpx import AsyncClient
from src.main import app
from src.core.dependencies import get_db, get_cache
from src.services.cache import CacheService
from src.models.database import Base, Vehicle
import uuid
from datetime import datetime
from decimal import Decimal


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_session() as session:
        await session.execute(text("DELETE FROM vehicles"))
        await session.commit()
        yield session
        await session.rollback()


@pytest.fixture
async def test_cache() -> CacheService:
    cache = CacheService(ttl=60)  
    await cache.connect()
    yield cache
    await cache.disconnect()


@pytest.fixture
async def client(test_session, test_cache) -> AsyncGenerator[AsyncClient, None]:
    
    async def override_get_db():
        yield test_session
    
    async def override_get_cache():
        return test_cache
    
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_cache] = override_get_cache
    
    async with AsyncClient(app=app, base_url="http://test/", follow_redirects=False) as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
async def sample_vehicles(test_session):
    vehicles = [
        Vehicle(
            id=uuid.uuid4(),
            brand="Toyota",
            model="Corolla",
            manufacture_year=2022,
            model_year=2023,
            engine_size=2.0,
            fuel_type="flex",
            color="branco",
            mileage=15000,
            doors=4,
            transmission="automatic",
            price=Decimal("95000.00"),
            created_at=datetime.utcnow()
        ),
        Vehicle(
            id=uuid.uuid4(),
            brand="Honda",
            model="Civic",
            manufacture_year=2021,
            model_year=2022,
            engine_size=1.5,
            fuel_type="gasoline",
            color="preto",
            mileage=25000,
            doors=4,
            transmission="manual",
            price=Decimal("85000.00"),
            created_at=datetime.utcnow()
        ),
        Vehicle(
            id=uuid.uuid4(),
            brand="Toyota",
            model="Hilux",
            manufacture_year=2023,
            model_year=2024,
            engine_size=2.8,
            fuel_type="diesel",
            color="branco metálico",
            mileage=5000,
            doors=4,
            transmission="automatic",
            price=Decimal("250000.00"),
            created_at=datetime.utcnow()
        ),
    ]
    
    for vehicle in vehicles:
        test_session.add(vehicle)
    
    await test_session.commit()
    
    for vehicle in vehicles:
        await test_session.refresh(vehicle)
    
    return vehicles