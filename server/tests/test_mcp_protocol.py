import pytest
from src.api.mcp.protocol import MCPRequest, MCPResponse, MCPProtocol, MCPError


def test_mcp_request_model():
    request = MCPRequest(
        method="tools/list",
        params={"test": "value"},
        id="123"
    )
    
    assert request.jsonrpc == "2.0"
    assert request.method == "tools/list"
    assert request.params == {"test": "value"}
    assert request.id == "123"


def test_mcp_response_model():
    response = MCPResponse(
        result={"data": "test"},
        id="123"
    )
    
    assert response.jsonrpc == "2.0"
    assert response.result == {"data": "test"}
    assert response.error is None
    assert response.id == "123"
    
    error_response = MCPResponse(
        error={"code": -32603, "message": "Internal error"},
        id="456"
    )
    
    assert error_response.result is None
    assert error_response.error["code"] == -32603


def test_create_error_response():
    response = MCPProtocol.create_error_response(
        MCPProtocol.METHOD_NOT_FOUND,
        "Method not found",
        request_id="123",
        data={"method": "unknown"}
    )
    
    assert response.jsonrpc == "2.0"
    assert response.error["code"] == -32601
    assert response.error["message"] == "Method not found"
    assert response.error["data"]["method"] == "unknown"
    assert response.id == "123"


def test_create_success_response():
    response = MCPProtocol.create_success_response(
        {"result": "data"},
        request_id="456"
    )
    
    assert response.jsonrpc == "2.0"
    assert response.result == {"result": "data"}
    assert response.error is None
    assert response.id == "456"


def test_get_tool_definitions():
    tools = MCPProtocol.get_tool_definitions()
    
    tool_names = [tool["name"] for tool in tools]
    expected_tools = [
        "search_vehicles",
        "list_brands",
        "list_models",
        "get_year_range",
        "get_price_range",
        "get_mileage_range",
        "list_available_colors",
        "list_fuel_types",
        "list_transmissions"
    ]
    
    assert all(name in tool_names for name in expected_tools)
    
    for tool in tools:
        assert "name" in tool
        assert "description" in tool
        assert "inputSchema" in tool
        assert tool["inputSchema"]["type"] == "object"
        assert "properties" in tool["inputSchema"]