import json
import time
from typing import Any, Optional, Callable, Dict, Tuple
import hashlib
import structlog

logger = structlog.get_logger()


class CacheService:
    
    def __init__(self, ttl: int = 3600):
        self.cache: Dict[str, Tuple[Any, float]] = {}
        self.default_ttl = ttl
    
    async def connect(self):
        logger.info("Initialized in-memory cache")
    
    async def disconnect(self):
        self.cache.clear()
        logger.info("Cleared in-memory cache")
    
    @staticmethod
    def generate_key(prefix: str, **params) -> str:
        param_str = json.dumps(params, sort_keys=True)
        hash_str = hashlib.md5(param_str.encode()).hexdigest()
        return f"{prefix}:{hash_str}"
    
    async def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            value, expires_at = self.cache[key]
            if time.time() < expires_at:
                return value
            else:
                del self.cache[key]
        return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        ttl = ttl or self.default_ttl
        expires_at = time.time() + ttl
        self.cache[key] = (value, expires_at)
        logger.debug("Cache set", key=key, ttl=ttl)
    
    async def get_or_set(
        self, 
        key: str, 
        func: Callable, 
        ttl: Optional[int] = None
    ) -> Any:
        value = await self.get(key)
        if value is not None:
            logger.debug("Cache hit", key=key)
            return value
        
        logger.debug("Cache miss", key=key)
        value = await func()
        await self.set(key, value, ttl)
        return value
    
    async def delete(self, key: str) -> None:
        if key in self.cache:
            del self.cache[key]
            logger.debug("Cache delete", key=key)
    
    async def clear_prefix(self, prefix: str) -> None:
        keys_to_delete = [key for key in self.cache.keys() if key.startswith(f"{prefix}:")]
        for key in keys_to_delete:
            del self.cache[key]
        logger.info("Cleared cache prefix", prefix=prefix, count=len(keys_to_delete))