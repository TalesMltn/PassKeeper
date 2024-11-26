import unittest
import re

class PasswordManager:
    def validate_password_length(self, password):
        # Verificar que la contraseña tenga al menos 12 caracteres y no más de 128
        return 12 <= len(password) <= 128

    def validate_password_strength(self, password):
        # Verificar que contenga mayúsculas, minúsculas, números y símbolos
        return (re.search(r'[A-Z]', password) and
                re.search(r'[a-z]', password) and
                re.search(r'[0-9]', password) and
                re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

    def validate_password_no_common_words(self, password):
        # Lista de palabras comunes a evitar en las contraseñas
        common_words = ["contraseña", "password", "123456", "qwerty"]
        return not any(word in password for word in common_words)

    def validate_password_no_names_or_brands(self, password):
        # Lista de nombres o marcas a evitar
        banned_names = ["Luis", "Nike", "Apple", "Microsoft"]
        return not any(name in password for name in banned_names)

    def validate_password_no_repeated_characters(self, password):
        # Verificar que la contraseña no tenga más de 3 caracteres repetidos
        # Usamos una expresión regular que busca cualquier carácter que se repita más de 3 veces
        return not any(password.count(char) > 3 for char in set(password))

    def validate_password_is_not_numeric_or_alpha(self, password):
        # Verificar que la contraseña no sea solo numérica o alfabética
        return not password.isdigit() and not password.isalpha()

    def validate_password_is_not_easy_sequence(self, password):
        # Verificar que la contraseña no sea una secuencia fácil como '1234', 'abcd'
        easy_sequences = ["1234", "abcd", "qwerty", "asdf", "zxcv"]
        return not any(seq in password for seq in easy_sequences)


class TestPasswordManager(unittest.TestCase):
    def setUp(self):
        # Crear la instancia de PasswordManager
        self.manager = PasswordManager()

    def test_password_length(self):
        # Verificar que la contraseña tenga al menos 12 caracteres y no más de 128 caracteres
        password = "A1b2C3d4E5f6"  # Contraseña válida
        self.assertTrue(self.manager.validate_password_length(password))
        password_too_short = "A1b2C3"  # Contraseña demasiado corta
        self.assertFalse(self.manager.validate_password_length(password_too_short))
        password_too_long = "A" * 129  # Contraseña demasiado larga
        self.assertFalse(self.manager.validate_password_length(password_too_long))

    def test_password_strength(self):
        # Verificar que la contraseña contenga mayúsculas, minúsculas, números y símbolos
        password = "A1b2C3d4E5f!6"  # Contraseña válida
        self.assertTrue(self.manager.validate_password_strength(password))
        password_weak = "abcdef123"  # Contraseña débil
        self.assertFalse(self.manager.validate_password_strength(password_weak))

    def test_password_no_common_words(self):
        # Verificar que la contraseña no contenga palabras comunes
        password = "A1b2C3d4E5f6"  # Contraseña válida
        self.assertTrue(self.manager.validate_password_no_common_words(password))
        password_common = "123456"  # Contraseña común
        self.assertFalse(self.manager.validate_password_no_common_words(password_common))

    def test_password_no_names_or_brands(self):
        # Verificar que la contraseña no contenga nombres ni marcas
        password = "A1b2C3d4E5f6"  # Contraseña válida
        self.assertTrue(self.manager.validate_password_no_names_or_brands(password))
        password_name = "Luis1234"  # Contraseña con un nombre
        self.assertFalse(self.manager.validate_password_no_names_or_brands(password_name))
        password_brand = "Apple1234"  # Contraseña con una marca
        self.assertFalse(self.manager.validate_password_no_names_or_brands(password_brand))

    def test_password_is_not_numeric_or_alpha(self):
        # Verificar que la contraseña no sea solo numérica o alfabética
        password_numeric = "123456789"  # Solo números
        self.assertFalse(self.manager.validate_password_is_not_numeric_or_alpha(password_numeric))
        password_alpha = "abcdefg"  # Solo letras
        self.assertFalse(self.manager.validate_password_is_not_numeric_or_alpha(password_alpha))
        password_mixed = "A1b2C3"  # Alfanumérica válida
        self.assertTrue(self.manager.validate_password_is_not_numeric_or_alpha(password_mixed))

    def test_password_is_not_easy_sequence(self):
        # Verificar que la contraseña no sea una secuencia fácil como '1234', 'abcd'
        password_easy = "1234"  # Secuencia fácil
        self.assertFalse(self.manager.validate_password_is_not_easy_sequence(password_easy))
        password_valid = "A1b2C3d4"  # Contraseña válida
        self.assertTrue(self.manager.validate_password_is_not_easy_sequence(password_valid))


if __name__ == '__main__':
    unittest.main()
