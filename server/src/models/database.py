from sqlalchemy import Column, String, Integer, Numeric, TIMESTAMP, text, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import TypeDecorator
import uuid


class TSVECTOR(TypeDecorator):
    impl = String
    cache_ok = True

@compiles(TSVECTOR, 'postgresql')
def compile_tsvector_postgresql(element, compiler, **kw):
    return "TSVECTOR"

Base = declarative_base()


class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    manufacture_year = Column(Integer, nullable=False)
    model_year = Column(Integer, nullable=False)
    engine_size = Column(Numeric(2, 1), nullable=False)
    fuel_type = Column(String(50), nullable=False)
    color = Column(String(50), nullable=False)
    mileage = Column(Integer, nullable=False)
    doors = Column(Integer, nullable=False)
    transmission = Column(String(50), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    search_vector = Column(TSVECTOR)

@event.listens_for(Vehicle.__table__, 'before_create')
def before_create(target, connection, **kw):
    if connection.dialect.name == 'postgresql':
        target.c.id.server_default = text("gen_random_uuid()")
        target.c.created_at.server_default = text("now() at time zone 'utc'")
