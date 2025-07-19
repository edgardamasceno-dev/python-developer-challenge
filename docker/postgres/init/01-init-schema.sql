-- Vehicle Database Schema for Python Developer Challenge
-- PostgreSQL 18 beta1-alpine
-- Simple schema focused on challenge requirements (10+ relevant attributes)

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS unaccent;

-- Main vehicles table with essential attributes
CREATE TABLE IF NOT EXISTS vehicles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    manufacture_year INTEGER NOT NULL,
    model_year INTEGER NOT NULL,
    engine_size NUMERIC(2, 1) NOT NULL,
    fuel_type VARCHAR(50) NOT NULL,
    color VARCHAR(50) NOT NULL,
    mileage INTEGER NOT NULL CHECK (mileage >= 0),
    doors INTEGER NOT NULL CHECK (doors IN (2, 3, 4, 5)),
    transmission VARCHAR(50) NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price > 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT (now() at time zone 'utc'),
    search_vector TSVECTOR,
    CONSTRAINT valid_years CHECK (
        manufacture_year >= 1990 AND 
        model_year >= manufacture_year AND 
        model_year <= EXTRACT(YEAR FROM now()) + 1
    )
);

-- Function to update full-text search vector for Portuguese
CREATE OR REPLACE FUNCTION update_vehicle_search_vector() RETURNS trigger AS $$
BEGIN
  NEW.search_vector := to_tsvector('portuguese', 
    unaccent(NEW.brand) || ' ' || 
    unaccent(NEW.model) || ' ' || 
    unaccent(NEW.color) || ' ' || 
    unaccent(NEW.fuel_type)
  );
  RETURN NEW;
END
$$ LANGUAGE plpgsql;

-- Trigger to automatically update search vector
CREATE TRIGGER update_search_vector 
    BEFORE INSERT OR UPDATE ON vehicles 
    FOR EACH ROW 
    EXECUTE FUNCTION update_vehicle_search_vector();

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_vehicles_brand_model ON vehicles (brand, model);
CREATE INDEX IF NOT EXISTS idx_vehicles_year ON vehicles (model_year DESC);
CREATE INDEX IF NOT EXISTS idx_vehicles_price ON vehicles (price);
CREATE INDEX IF NOT EXISTS idx_vehicles_search ON vehicles USING GIN(search_vector);
