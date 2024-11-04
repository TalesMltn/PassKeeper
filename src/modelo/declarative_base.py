# src/modelo/declarative_base.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Base de SQLAlchemy para todos los modelos
Base = declarative_base()

# Asegúrate de que la base de datos esté en una ubicación fija
db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite')
engine = create_engine(f'sqlite:///{db_path}', echo=False)

Session = sessionmaker(bind=engine)
session = Session()
