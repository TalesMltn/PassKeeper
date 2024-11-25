import sqlite3

class DBController:
    def __init__(self, db_path='../database/BDpasskeeper.db'):
        self.db_path = db_path

    def connect(self):
        """Conecta a la base de datos y retorna la conexión."""
        return sqlite3.connect(self.db_path)

    def buscar_usuario(self, usuario):
        """Busca si un usuario existe en la base de datos."""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario WHERE IDUser = ?", (usuario,))
            user = cursor.fetchone()
            conn.close()
            return user
        except sqlite3.Error as e:
            print("Error en la base de datos:", e)
            return None

    def actualizar_contraseña(self, usuario, nueva_contraseña):
        """Actualiza la contraseña de un usuario."""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE usuario SET Contraseña = ? WHERE IDUser = ?",
                (nueva_contraseña, usuario)
            )
            conn.commit()
            updated = cursor.rowcount > 0
            conn.close()
            return updated
        except sqlite3.Error as e:
            print("Error en la base de datos:", e)
            return False
