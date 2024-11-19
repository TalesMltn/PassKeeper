from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Aquí no debería haber validaciones específicas de correo
Base = declarative_base()
engine = create_engine('sqlite:///base_de_datos.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def crear_tablas():
    # Aquí simplemente creamos las tablas necesarias
    Base.metadata.create_all(engine)
