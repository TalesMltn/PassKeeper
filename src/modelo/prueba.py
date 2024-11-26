import sys


from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QLabel, QStackedWidget,
                             QMessageBox, QMainWindow, QTableWidget, QTableWidgetItem,
                             QDialog, QFormLayout)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize


class PasswordEntry(QDialog):
    def __init__(self, parent=None, service="", username="", password=""):
        super().__init__(parent)
        self.setWindowTitle("Entrada de Contraseña")
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: #9333EA;
                color: white;
            }
            QLineEdit {
                padding: 5px;
                border-radius: 3px;
                background-color: white;
                color: black;
            }
            QPushButton {
                padding: 5px 10px;
                border-radius: 3px;
                background-color: #7C3AED;
                color: white;
            }
            QPushButton:hover {
                background-color: #6D28D9;
            }
        """)

        layout = QFormLayout(self)

        self.service_input = QLineEdit(service)
        self.username_input = QLineEdit(username)
        self.password_input = QLineEdit(password)
        self.password_input.setEchoMode(QLineEdit.Password)

        layout.addRow("Servicio:", self.service_input)
        layout.addRow("Usuario:", self.username_input)
        layout.addRow("Contraseña:", self.password_input)

        buttons = QHBoxLayout()
        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)

        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)
        layout.addRow(buttons)

    def get_data(self):
        return (self.service_input.text(),
                self.username_input.text(),
                self.password_input.text())


class PasswordManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gestor de Contraseñas')
        self.setGeometry(100, 100, 800, 500)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #9333EA;
            }
            QTableWidget {
                background-color: white;
                color: black;
            }
            QTableWidget::item:selected {
                background-color: #7C3AED;
                color: white;
            }
            QPushButton {
                padding: 5px 10px;
                border-radius: 3px;
                background-color: #7C3AED;
                color: white;
            }
            QPushButton:hover {
                background-color: #6D28D9;
            }
        """)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Servicio', 'Usuario', 'Contraseña'])
        self.setCentralWidget(self.table)

        toolbar = self.addToolBar('Acciones')
        toolbar.setStyleSheet("""
            QToolBar {
                spacing: 10px;
                background-color: #7C3AED;
            }
        """)

        add_action = toolbar.addAction('Añadir')
        add_action.triggered.connect(self.add_password)

        edit_action = toolbar.addAction('Editar')
        edit_action.triggered.connect(self.edit_password)

        delete_action = toolbar.addAction('Eliminar')
        delete_action.triggered.connect(self.delete_password)

        self.load_passwords()

    def load_passwords(self):
        # Simular carga de contraseñas (en una aplicación real, esto vendría de una base de datos)
        passwords = [
            ('Google', 'usuario1@gmail.com', '********'),
            ('Facebook', 'usuario2@facebook.com', '********'),
            ('Twitter', 'usuario3@twitter.com', '********'),
        ]
        self.table.setRowCount(len(passwords))
        for row, (service, username, password) in enumerate(passwords):
            self.table.setItem(row, 0, QTableWidgetItem(service))
            self.table.setItem(row, 1, QTableWidgetItem(username))
            self.table.setItem(row, 2, QTableWidgetItem(password))

    def add_password(self):
        dialog = PasswordEntry(self)
        if dialog.exec_():
            service, username, password = dialog.get_data()
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(service))
            self.table.setItem(row_position, 1, QTableWidgetItem(username))
            self.table.setItem(row_position, 2, QTableWidgetItem('********'))

    def edit_password(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            service = self.table.item(current_row, 0).text()
            username = self.table.item(current_row, 1).text()
            password = '********'  # En una aplicación real, obtendríamos la contraseña real

            dialog = PasswordEntry(self, service, username, password)
            if dialog.exec_():
                new_service, new_username, new_password = dialog.get_data()
                self.table.setItem(current_row, 0, QTableWidgetItem(new_service))
                self.table.setItem(current_row, 1, QTableWidgetItem(new_username))
                self.table.setItem(current_row, 2, QTableWidgetItem('********'))

    def delete_password(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            confirm = QMessageBox.question(self, 'Confirmar eliminación',
                                           '¿Estás seguro de que quieres eliminar esta contraseña?',
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.table.removeRow(current_row)


class AuthSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sistema de Autenticación')
        self.setFixedSize(400, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #9333EA;
                color: white;
                font-size: 14px;
            }
            QLineEdit, QPushButton {
                padding: 10px;
                border-radius: 5px;
            }
            QLineEdit {
                background-color: white;
                color: black;
            }
            QPushButton {
                background-color: #7C3AED;
                border: none;
            }
            QPushButton:hover {
                background-color: #6D28D9;
            }
        """)

        self.stacked_widget = QStackedWidget()
        self.login_page = self.create_login_page()
        self.register_page = self.create_register_page()
        self.reset_page = self.create_reset_page()

        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.register_page)
        self.stacked_widget.addWidget(self.reset_page)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

    def create_login_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        icon_label = QLabel()
        pixmap = QPixmap("user_icon.png")  # Asegúrate de tener este archivo
        icon_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignCenter)

        title = QLabel("Iniciar Sesión")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        self.username = QLineEdit()
        self.username.setObjectName("username")
        self.username.setPlaceholderText("Usuario")
        self.password = QLineEdit()
        self.password.setObjectName("password")
        self.password.setPlaceholderText("Contraseña")
        self.password.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("Ingresar")
        login_button.clicked.connect(self.show_auto_logout_dialog)

        register_link = QPushButton("¿Es tu primera vez? Regístrate")
        register_link.setStyleSheet("background-color: transparent; text-decoration: underline;")
        register_link.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.register_page))

        forgot_password = QPushButton("¿Olvidaste la contraseña?")
        forgot_password.setStyleSheet("background-color: transparent; text-decoration: underline;")
        forgot_password.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.reset_page))

        layout.addWidget(icon_label)
        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(login_button)
        layout.addWidget(register_link)
        layout.addWidget(forgot_password)
        layout.addStretch()

        page.setLayout(layout)
        return page

    def create_register_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Registrar usuario")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        username = QLineEdit()
        username.setPlaceholderText("Crear Usuario")
        email = QLineEdit()
        email.setPlaceholderText("Correo electrónico")

        code_layout = QHBoxLayout()
        code = QLineEdit()
        code.setPlaceholderText("Código de verificación")
        generate_code = QPushButton("Generar por email")
        code_layout.addWidget(code)
        code_layout.addWidget(generate_code)

        password = QLineEdit()
        password.setPlaceholderText("Contraseña")
        password.setEchoMode(QLineEdit.Password)
        confirm_password = QLineEdit()
        confirm_password.setPlaceholderText("Confirmar contraseña")
        confirm_password.setEchoMode(QLineEdit.Password)

        register_button = QPushButton("Registrar")

        login_link = QPushButton("¿Ya estás registrado? Iniciar Sesión")
        login_link.setStyleSheet("background-color: transparent; text-decoration: underline;")
        login_link.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.login_page))

        layout.addWidget(title)
        layout.addWidget(username)
        layout.addWidget(email)
        layout.addLayout(code_layout)
        layout.addWidget(password)
        layout.addWidget(confirm_password)
        layout.addWidget(register_button)
        layout.addWidget(login_link)
        layout.addStretch()

        page.setLayout(layout)
        return page

    def create_reset_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Restablecer contraseña")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        email = QLineEdit()
        email.setPlaceholderText("Correo electrónico")

        code_layout = QHBoxLayout()
        code = QLineEdit()
        code.setPlaceholderText("Código de verificación")
        generate_code = QPushButton("Generar por email")
        code_layout.addWidget(code)
        code_layout.addWidget(generate_code)

        new_password = QLineEdit()
        new_password.setPlaceholderText("Contraseña")
        new_password.setEchoMode(QLineEdit.Password)
        confirm_password = QLineEdit()
        confirm_password.setPlaceholderText("Confirmar nueva contraseña")
        confirm_password.setEchoMode(QLineEdit.Password)

        reset_button = QPushButton("Restablecer")

        layout.addWidget(title)
        layout.addWidget(email)
        layout.addLayout(code_layout)
        layout.addWidget(new_password)
        layout.addWidget(confirm_password)
        layout.addWidget(reset_button)
        layout.addStretch()

        page.setLayout(layout)
        return page

    def authenticate_user(self, username, password):
        return username == "ALISTAR" and password == "ELFRIO"

    def show_auto_logout_dialog(self):
        if self.authenticate_user(self.username.text(), self.password.text()):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setText("CERRAR SESIÓN AUTOMÁTICA")
            msg.setInformativeText("¿Cerrar sesión automáticamente después de 10 min inactividad?")
            msg.setWindowTitle("Confirmación")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            result = msg.exec_()

            # Independientemente de la respuesta, lanzamos el gestor de contraseñas
            self.launch_password_manager()
        else:
            self.show_incorrect_password_dialog()

    def launch_password_manager(self):
        self.hide()  # Ocultar ventana de login
        self.password_manager = PasswordManager()
        self.password_manager.show()

    def show_incorrect_password_dialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("CLAVE INCORRECTA")
        msg.setInformativeText(
            "Después de tres intentos incorrectos el acceso se bloqueará. En caso no recuerdes tu contraseña, cambiala.")
        msg.setWindowTitle("Advertencia")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
if __name__ == '__main__':
        app = QApplication(sys.argv)
        auth_system = AuthSystem()
        auth_system.show()
        sys.exit(app.exec_())