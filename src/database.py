from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import settings

# Crear el motor de la base de datos
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)
# Crear la sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Declarative Base para definir los modelos
Base = declarative_base()