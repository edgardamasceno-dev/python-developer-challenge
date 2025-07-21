import pytest
import asyncio
import time
from src.services.cache import CacheService


@pytest.mark.asyncio
async def test_cache_set_and_get():
    cache = CacheService(ttl=60)
    await cache.connect()
    
    await cache.set("test_key", {"value": "test_data"})
    result = await cache.get("test_key")
    
    assert result == {"value": "test_data"}
    
    await cache.disconnect()


@pytest.mark.asyncio
async def test_cache_expiration():
    cache = CacheService(ttl=1)  
    await cache.connect()
    
    await cache.set("expire_key", "test_value", ttl=1)
    
    assert await cache.get("expire_key") == "test_value"
    
    await asyncio.sleep(1.1)
    
    assert await cache.get("expire_key") is None
    
    await cache.disconnect()


@pytest.mark.asyncio
async def test_cache_get_or_set():
    cache = CacheService(ttl=60)
    await cache.connect()
    
    call_count = 0
    
    async def expensive_function():
        nonlocal call_count
        call_count += 1
        return {"result": "expensive_data"}
    
    result1 = await cache.get_or_set("compute_key", expensive_function)
    assert result1 == {"result": "expensive_data"}
    assert call_count == 1
    
    result2 = await cache.get_or_set("compute_key", expensive_function)
    assert result2 == {"result": "expensive_data"}
    assert call_count == 1  
    
    await cache.disconnect()


@pytest.mark.asyncio
async def test_cache_delete():
    cache = CacheService(ttl=60)
    await cache.connect()
    
    await cache.set("delete_key", "test_value")
    assert await cache.get("delete_key") == "test_value"
    
    await cache.delete("delete_key")
    assert await cache.get("delete_key") is None
    
    await cache.disconnect()


@pytest.mark.asyncio
async def test_cache_clear_prefix():
    cache = CacheService(ttl=60)
    await cache.connect()
    
    await cache.set("prefix:key1", "value1")
    await cache.set("prefix:key2", "value2")
    await cache.set("other:key", "value3")
    
    await cache.clear_prefix("prefix")
    
    assert await cache.get("prefix:key1") is None
    assert await cache.get("prefix:key2") is None
    assert await cache.get("other:key") == "value3"
    
    await cache.disconnect()


@pytest.mark.asyncio
async def test_cache_generate_key():
    key1 = CacheService.generate_key("test", param1="value1", param2="value2")
    key2 = CacheService.generate_key("test", param2="value2", param1="value1")
    
    assert key1 == key2  
    assert key1.startswith("test:")
    
    key3 = CacheService.generate_key("test", param1="value3")
    assert key3 != key1