from sqlalchemy import Column, Integer, String
from src.modelo.declarative_base import Base

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    correo = Column(String, nullable=False)  # No aplicamos ninguna restricción aquí
    hash_contraseña = Column(String, nullable=False)

    def __repr__(self):
        return f"<Usuario(id={self.id}, correo={self.correo})>"
