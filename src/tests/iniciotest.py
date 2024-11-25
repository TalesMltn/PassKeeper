import unittest
from src.database.inicio import verificar_credenciales


class TestSimpleInicioSesion(unittest.TestCase):

    def test_credenciales_correctas(self):
        usuario = "tati"
        contrasena = "123"
        resultado = verificar_credenciales(usuario, contrasena)
        self.assertTrue(resultado, "Las credenciales correctas deberían retornar True.")

    def test_credenciales_incorrectas(self):
        usuario = "123"
        contrasena = "222"
        resultado = verificar_credenciales(usuario, contrasena)
        self.assertFalse(resultado, "Credenciales incorrectas deberían retornar False.")

    def test_campos_vacios(self):
        usuario = ""
        contrasena = ""
        resultado = verificar_credenciales(usuario, contrasena)
        self.assertFalse(resultado, "Campos vacíos deberían retornar False.")


if __name__ == '__main__':
    unittest.main()
