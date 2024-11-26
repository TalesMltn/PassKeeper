# declarative.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos SQLite
Base = declarative_base()
engine = create_engine('sqlite:///base_de_datos.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def crear_tablas():
    # Crear las tablas en la base de datos si no existen
    Base.metadata.create_all(engine)
