from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from src.api.mcp.protocol import MCPRequest, MCPResponse, MCPProtocol
from src.api.mcp.tools import VehicleMCPTools
from src.services.vehicle import VehicleService
from src.services.health import HealthService
from src.core.dependencies import get_vehicle_service, get_health_service
import structlog

logger = structlog.get_logger()

router = APIRouter(tags=["MCP"])


@router.post("/", response_model=MCPResponse)
async def handle_mcp_request(
    request: MCPRequest,
    vehicle_service: VehicleService = Depends(get_vehicle_service)
) -> MCPResponse:
    try:
        tools = VehicleMCPTools(vehicle_service)
        
        if request.method == "tools/list":
            result = {
                "tools": MCPProtocol.get_tool_definitions()
            }
            return MCPProtocol.create_success_response(result, request.id)
        
        elif request.method == "tools/call":
            tool_name = request.params.get("name")
            arguments = request.params.get("arguments", {})
            
            tool_methods = {
                "search_vehicles": tools.search_vehicles,
                "list_brands": tools.list_brands,
                "list_models": tools.list_models,
                "get_year_range": tools.get_year_range,
                "get_price_range": tools.get_price_range,
                "get_mileage_range": tools.get_mileage_range,
                "list_available_colors": tools.list_available_colors,
                "list_fuel_types": tools.list_fuel_types,
                "list_transmissions": tools.list_transmissions,
            }
            
            if tool_name not in tool_methods:
                return MCPProtocol.create_error_response(
                    MCPProtocol.METHOD_NOT_FOUND,
                    f"Tool '{tool_name}' not found",
                    request.id
                )
            
            try:
                result = await tool_methods[tool_name](**arguments)
                return MCPProtocol.create_success_response(
                    {"content": [{"type": "text", "text": str(result)}]},
                    request.id
                )
            except TypeError as e:
                return MCPProtocol.create_error_response(
                    MCPProtocol.INVALID_PARAMS,
                    str(e),
                    request.id
                )
        
        else:
            return MCPProtocol.create_error_response(
                MCPProtocol.METHOD_NOT_FOUND,
                f"Method '{request.method}' not found",
                request.id
            )
    
    except Exception as e:
        logger.error("MCP request failed", error=str(e), method=request.method)
        return MCPProtocol.create_error_response(
            MCPProtocol.INTERNAL_ERROR,
            "Internal server error",
            request.id,
            {"error": str(e)}
        )


@router.get("/health")
async def health_check(
    health_service: HealthService = Depends(get_health_service)
) -> Dict[str, Any]:
    return await health_service.get_health_status()