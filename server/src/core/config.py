from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "Vehicle MCP Server"
    app_version: str = "2.0.0"
    debug: bool = False
    
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    
    database_url: str
    db_pool_size: int = 20
    db_max_overflow: int = 40
    
    cache_ttl: int = 3600  
    
    mcp_endpoint: str = "/mcp"
    
    log_level: str = "INFO"
    
    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"

    def __init__(self, **values):
        super().__init__(**values)
        if self.database_url.startswith("sqlite"):
            self.db_pool_size = 1
            self.db_max_overflow = 0
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()