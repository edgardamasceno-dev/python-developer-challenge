# Python Developer Challenge

[English](#english) | [Português (BR)](#português-br)

---

# English

## Description

A terminal-based car search agent that helps users find vehicles through natural conversation. Built for the C2S Python Developer challenge using PostgreSQL, MCP protocol, and LLM integration.

See the full challenge: **[Challenge Description](./docs/challenge.md#english)**

## Vehicle Data Model

The database schema creates a `vehicles` table with 12+ attributes as required by the challenge:

```sql
CREATE TABLE vehicles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    manufacture_year INTEGER NOT NULL,
    model_year INTEGER NOT NULL,
    engine_size NUMERIC(2, 1) NOT NULL,
    fuel_type VARCHAR(50) NOT NULL,
    color VARCHAR(50) NOT NULL,
    mileage INTEGER NOT NULL,
    doors INTEGER NOT NULL,
    transmission VARCHAR(50) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT (now() at time zone 'utc'),
    search_vector TSVECTOR
);
```

Includes full-text search configured for Portuguese language and appropriate indexes for performance.

## Quick Start

### Prerequisites
- Python 3.8+
- Docker and Docker Compose

<<<<<<< Updated upstream
### Setup and Data Generation

1. **Setup Python environment and generate data**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   cd scripts
   pip install -r requirements.txt
   cd ..
   
   # Generate vehicle data (100-250 vehicles recommended)
   python scripts/generate_vehicle_data.py -n 150
   ```

2. **Configure and start database**
   ```bash
   # Setup environment
   cp .env.example .env
   # Edit .env with your database password
   
   # Start database
   docker-compose up
   ```

3. **Verify setup**
   ```bash
   # Check if table was created
   docker-compose exec database psql -U admin -d challenge_db -c "\dt"
   
   # Check if data was populated
   docker-compose exec database psql -U admin -d challenge_db -c "SELECT COUNT(*) FROM vehicles;"
   
   # View sample data
   docker-compose exec database psql -U admin -d challenge_db -c "SELECT brand, model, price FROM vehicles LIMIT 5;"
   ```

### Data Generation Options

```bash
# Generate with custom parameters
python scripts/generate_vehicle_data.py --help

# Examples:
python scripts/generate_vehicle_data.py -n 250              # 250 vehicles
python scripts/generate_vehicle_data.py -c custom.yaml      # Custom config
python scripts/generate_vehicle_data.py --seed 42           # Reproducible data
```

## Commands

```bash
# Stop
docker-compose down

# Connect to database
docker-compose exec database psql -U admin -d challenge_db
```

---

# Português (BR)

## Descrição

Agente de busca de carros baseado em terminal que ajuda usuários a encontrar veículos através de conversa natural. Desenvolvido para o desafio Python da C2S usando PostgreSQL, MCP protocolo e integração com LLM.

Veja o desafio completo: **[Descrição do Desafio](./docs/challenge.md#português-br)**

## Modelo de Dados dos Veículos

O schema do banco cria uma tabela `vehicles` com 12+ atributos conforme exigido pelo desafio:

```sql
CREATE TABLE vehicles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    manufacture_year INTEGER NOT NULL,
    model_year INTEGER NOT NULL,
    engine_size NUMERIC(2, 1) NOT NULL,
    fuel_type VARCHAR(50) NOT NULL,
    color VARCHAR(50) NOT NULL,
    mileage INTEGER NOT NULL,
    doors INTEGER NOT NULL,
    transmission VARCHAR(50) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT (now() at time zone 'utc'),
    search_vector TSVECTOR
);
```

Inclui busca textual completa configurada para português brasileiro e índices apropriados para performance.

## Como Rodar

### Pré-requisitos
- Python 3.8+
- Docker e Docker Compose

### Configuração e Geração de Dados

1. **Configurar ambiente Python e gerar dados**
   ```bash
   # Criar ambiente virtual
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   
   # Instalar dependências
   cd scripts
   pip install -r requirements.txt
   cd ..
   
   # Gerar dados dos veículos (100-250 veículos recomendado)
   python scripts/generate_vehicle_data.py -n 150
   ```

2. **Configurar e iniciar banco de dados**
   ```bash
   # Configurar ambiente
   cp .env.example .env
   # Edite o .env com sua senha do banco
   
   # Iniciar banco de dados
   docker-compose up
   ```

3. **Verificar configuração**
   ```bash
   # Verificar se a tabela foi criada
   docker-compose exec database psql -U admin -d challenge_db -c "\dt"
   
   # Verificar se foi populada com dados
   docker-compose exec database psql -U admin -d challenge_db -c "SELECT COUNT(*) FROM vehicles;"
   
   # Ver dados de exemplo
   docker-compose exec database psql -U admin -d challenge_db -c "SELECT brand, model, price FROM vehicles LIMIT 5;"
   ```

### Opções de Geração de Dados

```bash
# Gerar com parâmetros customizados
python scripts/generate_vehicle_data.py --help

# Exemplos:
python scripts/generate_vehicle_data.py -n 250              # 250 veículos
python scripts/generate_vehicle_data.py -c custom.yaml      # Config customizada
python scripts/generate_vehicle_data.py --seed 42           # Dados reproduzíveis
```

## Comandos

```bash
# Parar
docker-compose down

# Conectar ao banco
docker-compose exec database psql -U admin -d challenge_db
```