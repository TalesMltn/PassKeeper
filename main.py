# Definición de la clase Usuario
class Usuario:
    def __init__(self, id, correo, contraseña, autenticacion_dos_factores=False):
        self.id = id
        self.correo = correo
        self.contraseña = contraseña
        self.autenticacion_dos_factores = autenticacion_dos_factores
        self.contraseñas = []
        self.notificaciones = []
        self.recordatorios = []
        self.rol = None
        self.base_datos = None

    def registrar(self):
        print(f"Usuario {self.correo} registrado con éxito.")

    def iniciar_sesion(self):
        print(f"Usuario {self.correo} ha iniciado sesión.")

    def restablecer_contraseña(self, nueva_contraseña):
        self.contraseña = nueva_contraseña
        print(f"Contraseña restablecida para {self.correo}")

    def habilitar_dos_factores(self):
        self.autenticacion_dos_factores = True
        print(f"Autenticación de dos factores habilitada para {self.correo}")


# Clase Contraseña
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


# Clase Rol
class Rol:
    def __init__(self, id, nombre, descripcion):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion

    def asignar_rol(self, usuario):
        usuario.rol = self
        print(f"Rol {self.nombre} asignado a {usuario.correo}")


# Clase Notificación
class Notificacion:
    def __init__(self, id, usuario_id, contenido):
        self.id = id
        self.usuario_id = usuario_id
        self.contenido = contenido

    def enviar_notificacion(self):
        print(f"Notificación enviada: {self.contenido}")


# Clase Documento
class Documento:
    def __init__(self, id, nombre, fecha_creacion, estado, encriptado=False):
        self.id = id
        self.nombre = nombre
        self.fecha_creacion = fecha_creacion
        self.estado = estado
        self.encriptado = encriptado

    def subir(self):
        print(f"Documento {self.nombre} subido.")


# Función para registrar un usuario
def registrar_usuario():
    id = int(input("Ingresa el ID del usuario: "))
    correo = input("Ingresa el correo del usuario: ")
    contraseña = input("Ingresa la contraseña: ")
    autenticacion_dos_factores = input("¿Habilitar autenticación de dos factores? (s/n): ").lower() == 's'

    usuario = Usuario(id, correo, contraseña, autenticacion_dos_factores)
    usuario.registrar()
    return usuario


# Función para asignar un rol a un usuario
def asignar_rol(usuario):
    rol_id = int(input("Ingresa el ID del rol: "))
    nombre_rol = input("Ingresa el nombre del rol: ")
    descripcion_rol = input("Ingresa la descripción del rol: ")

    rol = Rol(rol_id, nombre_rol, descripcion_rol)
    rol.asignar_rol(usuario)


# Función para agregar una contraseña
def agregar_contraseña(usuario):
    id = int(input("Ingresa el ID de la contraseña: "))
    hash_contraseña = input("Ingresa la contraseña (hash): ")
    etiqueta = input("Ingresa una etiqueta para la contraseña: ")
    categoria = input("Ingresa la categoría de la contraseña: ")

    contraseña = Contraseña(id, usuario.id, hash_contraseña, etiqueta, categoria)
    contraseña.agregar_contraseña()
    usuario.contraseñas.append(contraseña)


# Función para enviar una notificación
def enviar_notificacion(usuario):
    notificacion_id = int(input("Ingresa el ID de la notificación: "))
    contenido = input("Ingresa el contenido de la notificación: ")

    notificacion = Notificacion(notificacion_id, usuario.id, contenido)
    notificacion.enviar_notificacion()
    usuario.notificaciones.append(notificacion)


# Función para subir un documento
def subir_documento():
    documento_id = int(input("Ingresa el ID del documento: "))
    nombre = input("Ingresa el nombre del documento: ")
    fecha_creacion = input("Ingresa la fecha de creación del documento (YYYY-MM-DD): ")
    estado = input("Ingresa el estado del documento: ")

    documento = Documento(documento_id, nombre, fecha_creacion, estado)
    documento.subir()


# Menú interactivo
def menu():
    usuario = registrar_usuario()

    while True:
        print("\n--- Menú de opciones ---")
        print("1. Asignar rol")
        print("2. Agregar contraseña")
        print("3. Enviar notificación")
        print("4. Subir documento")
        print("5. Salir")

        opcion = int(input("Selecciona una opción: "))

        if opcion == 1:
            asignar_rol(usuario)
        elif opcion == 2:
            agregar_contraseña(usuario)
        elif opcion == 3:
            enviar_notificacion(usuario)
        elif opcion == 4:
            subir_documento()
        elif opcion == 5:
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida, intenta de nuevo.")


# Ejecutar el menú
menu()
