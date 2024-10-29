from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from src.modelo.declarative_base import Base


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    correo = Column(String, nullable=False)
    hash_contraseña = Column(String, nullable=False)
    autenticacion_dos_factores = Column(String, nullable=False)
    articulos = relationship("Articulo", back_populates="usuario", cascade="all, delete-orphan")
    comentarios = relationship("Comentario", back_populates="usuario", cascade="all, delete-orphan")


class Articulo(Base):
    __tablename__ = 'articulos'

    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship("Usuario", back_populates="articulos")
    comentarios = relationship("Comentario", back_populates="articulo", cascade="all, delete-orphan")


class Comentario(Base):
    __tablename__ = 'comentarios'

    id = Column(Integer, primary_key=True)
    comentario = Column(String, nullable=False)
    articulo_id = Column(Integer, ForeignKey('articulos.id'))
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    articulo = relationship("Articulo", back_populates="comentarios")
    usuario = relationship("Usuario", back_populates="comentarios")
