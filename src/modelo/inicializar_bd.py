# src/modelo/inicializar_bd.py

from src.modelo.declarative_base import Base, engine
from src.modelo.modelo import Usuario, Articulo, Comentario

def inicializar_bd():
    Base.metadata.create_all(engine)
    print("Tablas creadas en la base de datos.")

if __name__ == "__main__":
    inicializar_bd()