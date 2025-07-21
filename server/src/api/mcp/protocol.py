from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
import json
import structlog

logger = structlog.get_logger()


class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: Dict[str, Any] = Field(default_factory=dict)
    id: Optional[str] = None


class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[str] = None


class MCPError(BaseModel):
    code: int
    message: str
    data: Optional[Dict[str, Any]] = None


class MCPProtocol:
    
    INTERNAL_ERROR = -32603
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    
    @staticmethod
    def create_error_response(
        error_code: int,
        message: str,
        request_id: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> MCPResponse:
        return MCPResponse(
            error=MCPError(
                code=error_code,
                message=message,
                data=data
            ).model_dump(),
            id=request_id
        )
    
    @staticmethod
    def create_success_response(
        result: Dict[str, Any],
        request_id: Optional[str] = None
    ) -> MCPResponse:
        return MCPResponse(
            result=result,
            id=request_id
        )
    
    @staticmethod
    def get_tool_definitions() -> List[Dict[str, Any]]:
        return [
            {
                "name": "search_vehicles",
                "description": "Search and filter vehicles in the catalog based on multiple criteria",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "search_text": {"type": "string", "description": "Full-text search query in Portuguese"},
                        "brand": {"type": "string", "description": "Filter by brand name"},
                        "model": {"type": "string", "description": "Filter by model name"},
                        "year_min": {"type": "integer", "description": "Minimum manufacturing year"},
                        "year_max": {"type": "integer", "description": "Maximum manufacturing year"},
                        "price_min": {"type": "number", "description": "Minimum price"},
                        "price_max": {"type": "number", "description": "Maximum price"},
                        "mileage_min": {"type": "integer", "description": "Minimum mileage (km)"},
                        "mileage_max": {"type": "integer", "description": "Maximum mileage (km)"},
                        "fuel_type": {"type": "string", "description": "Filter by fuel type"},
                        "color": {"type": "string", "description": "Filter by color (partial match)"},
                        "doors": {"type": "integer", "description": "Filter by number of doors"},
                        "transmission": {"type": "string", "description": "Filter by transmission type"},
                        "cursor": {"type": "string", "description": "Pagination cursor"},
                        "sort_by": {"type": "string", "description": "Sort field", "default": "id"},
                        "sort_order": {"type": "string", "description": "Sort order", "default": "asc"}
                    }
                }
            },
            {
                "name": "list_brands",
                "description": "Get a list of all vehicle brands available in the catalog",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "list_models",
                "description": "Get a list of vehicle models, optionally filtered by brand(s)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "brand": {
                            "oneOf": [
                                {"type": "string"},
                                {"type": "array", "items": {"type": "string"}}
                            ],
                            "description": "Single brand name or list of brand names to filter by"
                        }
                    }
                }
            },
            {
                "name": "get_year_range",
                "description": "Find the minimum and maximum manufacturing year",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_price_range",
                "description": "Find the minimum and maximum price",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_mileage_range",
                "description": "Find the minimum and maximum mileage",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "list_available_colors",
                "description": "Get a list of all unique vehicle colors",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "list_fuel_types",
                "description": "Get a list of all fuel types available",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "list_transmissions",
                "description": "Get a list of all transmission types available",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]