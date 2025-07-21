import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    response = await client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Vehicle MCP Server"
    assert "version" in data
    assert data["mcp_endpoint"] == "/mcp"


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient, sample_vehicles):
    response = await client.get("/mcp/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["checks"]["database_connection"] is True
    assert data["checks"]["vehicles_table"] is not None
    assert data["checks"]["cache_available"] is True


@pytest.mark.asyncio
async def test_mcp_tools_list(client: AsyncClient):
    request_data = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {},
        "id": "test-1"
    }
    
    response = await client.post("/mcp/", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["jsonrpc"] == "2.0"
    assert data["id"] == "test-1"
    assert "tools" in data["result"]
    assert len(data["result"]["tools"]) == 9  


@pytest.mark.asyncio
async def test_mcp_list_brands(client: AsyncClient, sample_vehicles):
    request_data = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "list_brands",
            "arguments": {}
        },
        "id": "test-2"
    }
    
    response = await client.post("/mcp/", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["jsonrpc"] == "2.0"
    assert data["id"] == "test-2"
    
    result_text = data["result"]["content"][0]["text"]
    assert "Honda" in result_text
    assert "Toyota" in result_text


@pytest.mark.asyncio
async def test_mcp_search_vehicles(client: AsyncClient, sample_vehicles):
    request_data = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "search_vehicles",
            "arguments": {
                "brand": "Toyota",
                "color": "branco"  
            }
        },
        "id": "test-3"
    }
    
    response = await client.post("/mcp/", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["jsonrpc"] == "2.0"
    assert data["id"] == "test-3"
    
    result_text = data["result"]["content"][0]["text"]
    assert "Toyota" in result_text
    assert "total_count" in result_text


@pytest.mark.asyncio
async def test_mcp_get_year_range(client: AsyncClient, sample_vehicles):
    request_data = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "get_year_range",
            "arguments": {}
        },
        "id": "test-4"
    }
    
    response = await client.post("/mcp/", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    result_text = data["result"]["content"][0]["text"]
    assert "min_year" in result_text
    assert "max_year" in result_text


@pytest.mark.asyncio
async def test_mcp_invalid_method(client: AsyncClient):
    request_data = {
        "jsonrpc": "2.0",
        "method": "invalid/method",
        "params": {},
        "id": "test-error-1"
    }
    
    response = await client.post("/mcp/", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["error"]["code"] == -32601  
    assert "not found" in data["error"]["message"]


@pytest.mark.asyncio
async def test_mcp_invalid_tool(client: AsyncClient):
    request_data = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "invalid_tool",
            "arguments": {}
        },
        "id": "test-error-2"
    }
    
    response = await client.post("/mcp/", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["error"]["code"] == -32601  
    assert "not found" in data["error"]["message"]


@pytest.mark.asyncio
async def test_mcp_invalid_params(client: AsyncClient):
    request_data = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "search_vehicles",
            "arguments": {
                "invalid_param": "value"  
            }
        },
        "id": "test-error-3"
    }
    
    response = await client.post("/mcp/", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == -32602  # Invalid params