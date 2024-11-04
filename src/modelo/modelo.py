# src/modelo/modelo.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.modelo.declarative_base import Base, session


# Modelo Usuario
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    correo = Column(String, nullable=False, unique=True)
    hash_contraseña = Column(String, nullable=False)
    autenticacion_dos_factores = Column(String, nullable=False)
    articulos = relationship("Articulo", back_populates="usuario", cascade="all, delete-orphan")
    comentarios = relationship("Comentario", back_populates="usuario", cascade="all, delete-orphan")


# Modelo Articulo
class Articulo(Base):
    __tablename__ = 'articulos'

    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship("Usuario", back_populates="articulos")
    comentarios = relationship("Comentario", back_populates="articulo", cascade="all, delete-orphan")


# Modelo Comentario
class Comentario(Base):
    __tablename__ = 'comentarios'

    id = Column(Integer, primary_key=True)
    comentario = Column(String, nullable=False)
    articulo_id = Column(Integer, ForeignKey('articulos.id'))
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    articulo = relationship("Articulo", back_populates="comentarios")
    usuario = relationship("Usuario", back_populates="comentarios")


# Clase de gestión de artículos y comentarios
class ArticuloManager:
    def __init__(self):
        self.session = session

    def crear_articulo(self, usuario, titulo):
        articulo = Articulo(titulo=titulo, usuario=usuario)
        self.session.add(articulo)
        self.session.commit()
        usuario.articulos.append(articulo)
        return articulo

    def leer_articulo(self, articulo_id):
        return self.session.query(Articulo).filter_by(id=articulo_id).first()

    def actualizar_articulo(self, articulo_id, nuevo_titulo):
        articulo = self.leer_articulo(articulo_id)
        if articulo:
            articulo.titulo = nuevo_titulo
            self.session.commit()
        return articulo

    def eliminar_articulo(self, articulo_id):
        articulo = self.leer_articulo(articulo_id)
        if articulo:
            self.session.delete(articulo)
            self.session.commit()
        return articulo

    def agregar_comentario(self, usuario, articulo_id, comentario_texto):
        articulo = self.leer_articulo(articulo_id)
        if articulo:
            comentario = Comentario(comentario=comentario_texto, articulo=articulo, usuario=usuario)
            self.session.add(comentario)
            self.session.commit()
            usuario.comentarios.append(comentario)
            return comentario
        return None

    def leer_comentarios(self, articulo_id):
        articulo = self.leer_articulo(articulo_id)
        return articulo.comentarios if articulo else None
