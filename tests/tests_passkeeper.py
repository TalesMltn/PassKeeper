import unittest
from PyQt5.QtWidgets import QApplication
from src.logica.main import PasswordManager

class TestPasswordManager(unittest.TestCase):
    def setUp(self):
        # Crear la instancia de la aplicación Qt antes de las pruebas
        self.app = QApplication([])
        # Crear la instancia de PasswordManager
        self.manager = PasswordManager()

    def test_init(self):
        # Verificar que el título de la ventana es el esperado
        self.assertEqual(self.manager.windowTitle(), "Gestor de Contraseñas")

    def test_add_password(self):
        # Verificar que la función de agregar contraseñas esté funcionando correctamente
        initial_row_count = self.manager.table.rowCount()
        self.manager.add_password()  # Simula la adición de una nueva contraseña
        # Comprobar que el número de filas ha aumentado
        self.assertGreater(self.manager.table.rowCount(), initial_row_count)

    def test_edit_password(self):
        # Suponiendo que ya hay al menos una entrada en la tabla
        self.manager.add_password()  # Asegurarse de que al menos una fila exista
        current_row = self.manager.table.rowCount() - 1
        # Editar una contraseña existente
        self.manager.edit_password()
        # Verificar que el número de filas no cambió (se edita la fila, no se agrega una nueva)
        self.assertEqual(self.manager.table.rowCount(), current_row)

    def test_delete_password(self):
        # Asegurarse de que haya al menos una contraseña antes de intentar eliminar
        self.manager.add_password()
        initial_row_count = self.manager.table.rowCount()
        self.manager.delete_password()
        # Verificar que el número de filas se haya reducido
        self.assertLess(self.manager.table.rowCount(), initial_row_count)

if __name__ == '__main__':
    unittest.main()

