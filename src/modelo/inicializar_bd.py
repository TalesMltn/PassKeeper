# inicializar.py
from src.modelo.declarative_base import Base, engine

def inicializar_bd():
    # Crear las tablas en la base de datos si no existen
    Base.metadata.create_all(engine)
