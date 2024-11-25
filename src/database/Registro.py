import sqlite3
import os
from tkinter import messagebox


DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "BDpasskeeper.db"))

def registrar_usuario_bd(nombre, contrasena, correo):
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO usuario (IDUser, Contraseña, Correo) VALUES (?, ?, ?)",
            (nombre, contrasena, correo)
        )
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar en la base de datos: {e}")
        return False  # Operación fallida
