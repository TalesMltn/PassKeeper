import sqlite3
import os
from tkinter import messagebox

# Ruta de la base de datos
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "BDpasskeeper.db"))

def obtener_conexion():
    """Establece una conexión con la base de datos."""
    try:
        conexion = sqlite3.connect(DB_PATH)
        return conexion
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

def verificar_credenciales(usuario, contrasena):
    """
    Verifica si un usuario y contraseña son válidos en la base de datos.
    :param usuario: Nombre del usuario.
    :param contrasena: Contraseña del usuario.
    :return: True si las credenciales son válidas, False en caso contrario.
    """
    try:
        conexion = obtener_conexion()
        if not conexion:
            return False

        cursor = conexion.cursor()
        query = "SELECT * FROM usuario WHERE IDUser = ? AND Contraseña = ?"
        cursor.execute(query, (usuario, contrasena))
        resultado = cursor.fetchone()
        conexion.close()

        return resultado is not None
    except sqlite3.Error as e:
        print(f"Error al realizar la consulta: {e}")
        return False
