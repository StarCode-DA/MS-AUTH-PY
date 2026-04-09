from sqlalchemy import Column, Integer, String
from src.database import Base

class Administrador(Base):
    __tablename__ = "administradores"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)