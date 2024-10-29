from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configurar base de datos SQLite en memoria para las pruebas
engine = create_engine('sqlite:///db.sqlite', echo=False)
# engine = create_engine('sqlite:///', echo=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()
session = Session()

