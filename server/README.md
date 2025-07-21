# MCP Vehicle Server

[English](#english) | [Português (BR)](#português-br)

---

# English

Model Context Protocol server for vehicle search and filtering operations with in-memory caching and PostgreSQL backend.

## Key Features

- MCP protocol implementation for LLM integration
- In-memory caching for performance optimization
- UUID v7 cursor-based pagination
- Portuguese full-text search support
- Health checks for database connectivity
- Partial color matching (e.g., "branco" matches "branco metálico")


## API Reference

### MCP Tools

Access via `/mcp` endpoint using MCP protocol:

- **search_vehicles**: Search and filter vehicles with pagination
- **list_brands**: Get all available brands
- **list_models**: Get models (optionally filtered by brands)
- **get_year_range**: Get min/max manufacturing years
- **get_price_range**: Get min/max prices
- **get_mileage_range**: Get min/max mileage
- **list_available_colors**: Get all available colors
- **list_fuel_types**: Get all fuel types
- **list_transmissions**: Get all transmission types

### Health Check

`GET /mcp/health` - Verifies database connection and vehicles table existence.

## Development

```bash
# Local setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python run.py

# Docker (included in main docker-compose.yml)
docker-compose up
docker-compose logs -f server
```

---

# Português (BR)

Servidor do protocolo MCP para operações de busca e filtragem de veículos com cache em memória e backend PostgreSQL.

## Principais Funcionalidades

- Implementação do protocolo MCP para integração com LLM
- Cache em memória para otimização de performance
- Paginação baseada em cursor UUID v7
- Suporte a busca textual completa em português
- Verificações de saúde para conectividade do banco
- Busca parcial de cores (ex: "branco" encontra "branco metálico")


## Referência da API

### Ferramentas MCP

Acesso via endpoint `/mcp` usando protocolo MCP:

- **search_vehicles**: Buscar e filtrar veículos com paginação
- **list_brands**: Obter todas as marcas disponíveis
- **list_models**: Obter modelos (opcionalmente filtrados por marcas)
- **get_year_range**: Obter anos mínimo/máximo de fabricação
- **get_price_range**: Obter preços mínimo/máximo
- **get_mileage_range**: Obter quilometragem mínima/máxima
- **list_available_colors**: Obter todas as cores disponíveis
- **list_fuel_types**: Obter todos os tipos de combustível
- **list_transmissions**: Obter todos os tipos de transmissão

### Verificação de Saúde

`GET /mcp/health` - Verifica conexão com banco e existência da tabela vehicles.

## Desenvolvimento

```bash
# Configuração local
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python run.py

# Docker (incluído no docker-compose.yml principal)
docker-compose up
docker-compose logs -f server
```