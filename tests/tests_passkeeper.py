# tests_passkeeper.py
import unittest
import re

class PasswordManager:
    """
    Clase para gestionar la validación de contraseñas según múltiples criterios.
    """
    def validate_password_length(self, password):
        # Verifica que la contraseña tenga entre 12 y 128 caracteres.
        return 12 <= len(password) <= 128

    def validate_password_strength(self, password):
        # Comprueba que la contraseña tenga mayúsculas, minúsculas, números y símbolos especiales.
        return (re.search(r'[A-Z]', password) and
                re.search(r'[a-z]', password) and
                re.search(r'[0-9]', password) and
                re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

    def validate_password_no_common_words(self, password):
        # Verifica que no contenga palabras comunes como "contraseña" o "123456".
        common_words = ["contraseña", "password", "123456", "qwerty"]
        return not any(word in password.lower() for word in common_words)

    def validate_password_no_names_or_brands(self, password):
        # Asegura que no contenga nombres propios o marcas conocidas.
        banned_names = ["Luis", "Nike", "Apple", "Microsoft"]
        return not any(name.lower() in password.lower() for name in banned_names)

    def validate_password_no_repeated_characters(self, password):
        # Comprueba que ningún carácter se repita más de 3 veces.
        return not any(password.count(char) > 3 for char in set(password))

    def validate_password_is_not_numeric_or_alpha(self, password):
        # Verifica que la contraseña no sea solo numérica o solo alfabética.
        return not password.isdigit() and not password.isalpha()

    def validate_password_is_not_easy_sequence(self, password):
        # Asegura que no sea una secuencia fácil como "1234" o "abcd".
        easy_sequences = ["1234", "abcd", "qwerty", "asdf", "zxcv"]
        return not any(seq in password.lower() for seq in easy_sequences)

    def validate_password_no_spaces(self, password):
        # Verifica que no contenga espacios en blanco.
        return ' ' not in password

    def validate_password_is_not_repetitive_pattern(self, password):
        # Comprueba que no sea un patrón repetitivo como "abababab".
        return not re.search(r'(.+)\1{2,}', password)

    def validate_password_differs_from_context(self, password, username, service):
        # Asegura que la contraseña no sea igual al nombre de usuario o al nombre del servicio.
        return password.lower() not in {username.lower(), service.lower()}

class TestPasswordManager(unittest.TestCase):
    """
    Clase para probar las validaciones del gestor de contraseñas.
    """
    def setUp(self):
        # Configuración inicial: se crea una instancia de PasswordManager.
        self.manager = PasswordManager()

    def test_password_length(self):
        # Verifica que las contraseñas cumplan con el rango de longitud permitido.
        self.assertTrue(self.manager.validate_password_length("A1b2C3d4E5f6"))
        self.assertFalse(self.manager.validate_password_length("Short12"))
        self.assertFalse(self.manager.validate_password_length("A" * 129))

    def test_password_strength(self):
        # Asegura que las contraseñas incluyan letras, números y símbolos.
        self.assertTrue(self.manager.validate_password_strength("StrongPass1!"))
        self.assertFalse(self.manager.validate_password_strength("weakpassword"))

    def test_password_no_common_words(self):
        # Verifica que no contenga palabras comunes (como "password").
        self.assertTrue(self.manager.validate_password_no_common_words("JoseBacilio1!"))
        self.assertFalse(self.manager.validate_password_no_common_words("UniquePassword1!"))
        self.assertFalse(self.manager.validate_password_no_common_words("password123"))

    def test_password_no_names_or_brands(self):
        # Asegura que no incluya nombres propios o marcas conocidas.
        self.assertTrue(self.manager.validate_password_no_names_or_brands("CustomPass1!"))
        self.assertFalse(self.manager.validate_password_no_names_or_brands("NikePassword123"))

    def test_password_no_repeated_characters(self):
        # Comprueba que ningún carácter se repita más de 3 veces.
        self.assertTrue(self.manager.validate_password_no_repeated_characters("Valid1!"))
        self.assertFalse(self.manager.validate_password_no_repeated_characters("AaaaAAB1!"))

    def test_password_is_not_numeric_or_alpha(self):
        # Verifica que la contraseña no sea solo numérica o solo alfabética.
        self.assertTrue(self.manager.validate_password_is_not_numeric_or_alpha("Mix123!"))
        self.assertFalse(self.manager.validate_password_is_not_numeric_or_alpha("12345678"))
        self.assertFalse(self.manager.validate_password_is_not_numeric_or_alpha("abcdefg"))

    def test_password_is_not_easy_sequence(self):
        # Asegura que no sea una secuencia fácil como "1234" o "abcd".
        self.assertTrue(self.manager.validate_password_is_not_easy_sequence("Complex1!"))
        self.assertFalse(self.manager.validate_password_is_not_easy_sequence("1234abcd"))

    def test_password_no_spaces(self):
        # Verifica que la contraseña no contenga espacios en blanco.
        self.assertTrue(self.manager.validate_password_no_spaces("NoSpaces1!"))
        self.assertFalse(self.manager.validate_password_no_spaces("With Space1!"))

    def test_password_is_not_repetitive_pattern(self):
        # Comprueba que no sea un patrón repetitivo (como "abababab").
        self.assertTrue(self.manager.validate_password_is_not_repetitive_pattern("NoPattern1!"))
        self.assertFalse(self.manager.validate_password_is_not_repetitive_pattern("abababab"))

    def test_password_differs_from_context(self):
        # Asegura que la contraseña no sea igual al usuario o al servicio.
        self.assertTrue(self.manager.validate_password_differs_from_context("Valid1!", "user", "service"))
        self.assertFalse(self.manager.validate_password_differs_from_context("service", "user", "service"))

if __name__ == '__main__':
    unittest.main()
