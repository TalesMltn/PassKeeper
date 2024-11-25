import sqlite3
import os

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

def obtener_datos_passkeeper(id_usuario):
    """
    Obtiene los datos de la tabla PassKeeper para un usuario específico.
    :param id_usuario: ID del usuario logueado.
    :return: Lista de registros (tuplas) obtenidos de la tabla PassKeeper.
    """
    try:
        conexion = obtener_conexion()
        if not conexion:
            return []

        cursor = conexion.cursor()
        query = """
        SELECT Usuario_Pass, Contraseña_Pass, SitioWeb, Seguridad 
        FROM PassKeeper 
        WHERE IDUser = ?
        """
        cursor.execute(query, (id_usuario,))
        datos = cursor.fetchall()
        conexion.close()
        return datos
    except sqlite3.Error as e:
        print(f"Error al obtener los datos: {e}")
        return []
