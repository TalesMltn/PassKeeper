import sqlite3

try:
    # Conexión a la base de datos
    mi_conexion = sqlite3.connect("BDpasskeeper.db")  # Asegúrate de agregar la extensión .db
    mi_conexion.execute("PRAGMA foreign_keys = 1")  # Habilitar soporte para claves foráneas
    cursor = mi_conexion.cursor()

    # Crear la tabla usuario
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (    
        IDUser VARCHAR(200) PRIMARY KEY,
        Contraseña VARCHAR(200),
        Correo VARCHAR(200)
    )
    """)

    # Crear la tabla PassKeeper
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS PassKeeper (
        IDPasskeeper INTEGER PRIMARY KEY AUTOINCREMENT,
        Usuario_Pass VARCHAR(200),
        Contraseña_Pass VARCHAR(200),
        SitioWeb VARCHAR(200),
        Seguridad VARCHAR(50),
        IDUser VARCHAR(200),
        FOREIGN KEY(IDUser) REFERENCES usuario(IDUser) ON DELETE CASCADE
    )
    """)

    # Insertar un usuario en la tabla usuario (previamente necesario para las claves foráneas)
    cursor.execute("""
    INSERT OR IGNORE INTO usuario (IDUser, Contraseña, Correo)
    VALUES ('tati', '123', 'correo@example.com')
    """)

    # Insertar datos en la tabla PassKeeper
    cursor.execute("""
    INSERT INTO PassKeeper (Usuario_Pass, Contraseña_Pass, SitioWeb, Seguridad, IDUser)
    VALUES ('tati', 'micontraseña1', 'example.com', 'Alta', 'tati')
    """)

    cursor.execute("""
    INSERT INTO PassKeeper (Usuario_Pass, Contraseña_Pass, SitioWeb, Seguridad, IDUser)
    VALUES ('josu', 'micontraseña2', 'example.org', 'Media', 'josu')
    """)

    # Confirmar cambios
    mi_conexion.commit()
    print("Datos insertados con éxito")

except Exception as ex:
    print("Ocurrió un error:", ex)

finally:
    # Cerrar la conexión
    if 'mi_conexion' in locals():
        mi_conexion.close()
