# modelo.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///base_de_datos.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Modelo de la tabla de contraseñas
class Password(Base):
    __tablename__ = 'passwords'
    id = Column(Integer, primary_key=True, autoincrement=True)
    service = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

# Crear las tablas si no existen
Base.metadata.create_all(engine)


class Usuario:
    __tablename__ = 'passwords'
    id = Column(Integer, primary_key=True, autoincrement=True)
    service = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

Base.metadata.create_all(engine)