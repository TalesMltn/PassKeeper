# src/logica/main.py

from src.modelo.modelo import Usuario, ArticuloManager
from src.modelo.declarative_base import session


def registrar_usuario():
    id = int(input("Ingresa el ID del usuario: "))
    correo = input("Ingresa el correo del usuario: ")
    hash_contraseña = input("Ingresa la contraseña (hash): ")
    autenticacion_dos_factores = input("¿Habilitar autenticación de dos factores? (s/n): ").lower() == 's'

    usuario = Usuario(
        id=id,
        correo=correo,
        hash_contraseña=hash_contraseña,
        autenticacion_dos_factores=autenticacion_dos_factores
    )
    session.add(usuario)
    session.commit()
    print(f"Usuario {usuario.correo} registrado con éxito.")
    return usuario


def menu():
    articulo_manager = ArticuloManager()
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
            articulo_manager.crear_articulo(usuario, titulo)
        elif opcion == 2:
            articulo_id = int(input("Ingresa el ID del artículo a leer: "))
            articulo = articulo_manager.leer_articulo(articulo_id)
            print(articulo.titulo if articulo else "Artículo no encontrado.")
        elif opcion == 3:
            articulo_id = int(input("Ingresa el ID del artículo a actualizar: "))
            nuevo_titulo = input("Ingresa el nuevo título: ")
            articulo_manager.actualizar_articulo(articulo_id, nuevo_titulo)
        elif opcion == 4:
            articulo_id = int(input("Ingresa el ID del artículo a eliminar: "))
            articulo_manager.eliminar_articulo(articulo_id)
        elif opcion == 5:
            articulo_id = int(input("Ingresa el ID del artículo para comentar: "))
            comentario_texto = input("Ingresa el comentario: ")
            articulo_manager.agregar_comentario(usuario, articulo_id, comentario_texto)
        elif opcion == 6:
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    menu()
