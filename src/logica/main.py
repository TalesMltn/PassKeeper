class Usuario:
    def __init__(self, id, correo, hash_contraseña, autenticacion_dos_factores=False):
        self.id = id
        self.correo = correo
        self.hash_contraseña = hash_contraseña
        self.autenticacion_dos_factores = autenticacion_dos_factores
        self.contraseñas = []
        self.notificaciones = []
        self.recordatorios = []
        self.rol = None
        self.articulos = []
        self.comentarios = []

    def registrar(self):
        print(f"Usuario {self.correo} registrado con éxito.")

    def iniciar_sesion(self):
        print(f"Usuario {self.correo} ha iniciado sesión.")

    def restablecer_contraseña(self, nueva_contraseña):
        self.hash_contraseña = nueva_contraseña
        print(f"Contraseña restablecida para {self.correo}")

    def habilitar_dos_factores(self):
        self.autenticacion_dos_factores = True
        print(f"Autenticación de dos factores habilitada para {self.correo}")


class Contraseña:
    def __init__(self, id, usuario_id, hash_contraseña, etiqueta, categoria):
        self.id = id
        self.usuario_id = usuario_id
        self.hash_contraseña = hash_contraseña
        self.etiqueta = etiqueta
        self.categoria = categoria
        self.historial = []

    def agregar_contraseña(self):
        print(f"Contraseña {self.etiqueta} agregada.")

    def editar_contraseña(self, nueva_contraseña):
        self.hash_contraseña = nueva_contraseña
        print(f"Contraseña {self.etiqueta} editada.")

    def eliminar_contraseña(self):
        print(f"Contraseña {self.etiqueta} eliminada.")

    def obtener_historial(self):
        return self.historial


class ArticuloManager:
    def __init__(self, session):
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


# Base de datos y Sesión SQLAlchemy
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
articuloManager = ArticuloManager(session)


# Menú Interactivo
def menu():
    usuario = registrar_usuario()
    while True:
        print("\n--- Menú de opciones ---")
        print("1. Crear artículo")
        print("2. Leer artículo")
        print("3. Actualizar artículo")
        print("4. Eliminar artículo")
        print("5. Agregar comentario")
        print("6. Salir")

        opcion = int(input("Selecciona una opción: "))

        if opcion == 1:
            titulo = input("Ingresa el título del artículo: ")
            articuloManager.crear_articulo(usuario, titulo)
        elif opcion == 2:
            articulo_id = int(input("Ingresa el ID del artículo a leer: "))
            articulo = articuloManager.leer_articulo(articulo_id)
            print(articulo.titulo if articulo else "Artículo no encontrado.")
        elif opcion == 3:
            articulo_id = int(input("Ingresa el ID del artículo a actualizar: "))
            nuevo_titulo = input("Ingresa el nuevo título: ")
            articuloManager.actualizar_articulo(articulo_id, nuevo_titulo)
        elif opcion == 4:
            articulo_id = int(input("Ingresa el ID del artículo a eliminar: "))
            articuloManager.eliminar_articulo(articulo_id)
        elif opcion == 5:
            articulo_id = int(input("Ingresa el ID del artículo para comentar: "))
            comentario_texto = input("Ingresa el comentario: ")
            articuloManager.agregar_comentario(usuario, articulo_id, comentario_texto)
        elif opcion == 6:
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida, intenta de nuevo.")


# Ejecutar el menú
menu()