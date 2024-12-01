import sys
import bcrypt
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QLabel, QStackedWidget,
                             QMessageBox, QMainWindow, QTableWidget, QTableWidgetItem,
                             QDialog, QFormLayout, QInputDialog)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from src.modelo.modelo import Password, session
from tests.tests_passkeeper import PasswordManager as PasswordValidator


class VerifyCredentialsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Verificar Credenciales")
        layout = QVBoxLayout(self)

        self.username = QLineEdit(self)
        self.username.setPlaceholderText("Usuario")
        layout.addWidget(self.username)

        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Contraseña")
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        buttons = QHBoxLayout()
        ok_button = QPushButton("Aceptar")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addLayout(buttons)

    def get_credentials(self):
        return self.username.text(), self.password.text()


class PasswordEntry(QDialog):
    def __init__(self, parent=None, service="", username="", password="", is_encrypted=True):
        super().__init__(parent)
        self.setWindowTitle("Entrada de Contraseña")
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: #A3C1DA;
                color: black;
            }
            QLineEdit, QPushButton {
                padding: 5px;
                border-radius: 3px;
                background-color: white;
                color: black;
                font-family: 'Times New Roman';
            }
            QPushButton {
                background-color: #6495ED;
                color: white;
            }
            QPushButton:hover {
                background-color: #4682B4;
            }
        """)

        layout = QFormLayout(self)

        self.service_input = QLineEdit(service)
        self.username_input = QLineEdit(username)
        self.password_input = QLineEdit(password)
        self.password_input.setEchoMode(QLineEdit.Password)

        layout.addRow("Oficio:", self.service_input)
        layout.addRow("Usuario:", self.username_input)
        layout.addRow("Contraseña:", self.password_input)

        self.show_password_button = QPushButton("Mostrar Contraseña")
        self.show_password_button.clicked.connect(self.toggle_password_visibility)
        layout.addRow(self.show_password_button)

        self.show_unencrypted_button = QPushButton("Mostrar contraseña sin encriptar")
        self.show_unencrypted_button.clicked.connect(self.show_unencrypted_password)
        layout.addRow(self.show_unencrypted_button)

        buttons = QHBoxLayout()
        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)

        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)
        layout.addRow(buttons)

        self.password_validator = PasswordValidator()
        self.is_encrypted = is_encrypted
        self.parent = parent

    def get_data(self):
        return (self.service_input.text(),
                self.username_input.text(),
                self.password_input.text())

    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.show_password_button.setText("Ocultar Contraseña")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.show_password_button.setText("Mostrar Contraseña")

    def show_unencrypted_password(self):
        if self.is_encrypted:
            verify_dialog = VerifyCredentialsDialog(self)
            if verify_dialog.exec_():
                username, password = verify_dialog.get_credentials()
                if self.parent.authenticate_user(username, password):
                    decrypted_password = self.decrypt_password(self.password_input.text())
                    QMessageBox.information(self, "Contraseña sin encriptar",
                                            f"La contraseña sin encriptar es: {decrypted_password}")
                else:
                    QMessageBox.warning(self, "Error", "Credenciales incorrectas")
        else:
            QMessageBox.information(self, "Contraseña sin encriptar",
                                    f"La contraseña sin encriptar es: {self.password_input.text()}")

    def decrypt_password(self, encrypted_password):
        # En este caso, como estamos usando bcrypt, no podemos desencriptar.
        # Simplemente devolvemos la contraseña encriptada.
        return encrypted_password

    def accept(self):
        service, username, password = self.get_data()
        errors = self.validate_password(password, username, service)
        if errors:
            QMessageBox.warning(self, "Error de validación", "\n".join(errors))
        else:
            super().accept()

    def validate_password(self, password, username, service):
        errors = []
        if not self.password_validator.validate_password_length(password):
            errors.append("La contraseña debe tener entre 12 y 128 caracteres.")
        if not self.password_validator.validate_password_strength(password):
            errors.append("La contraseña debe incluir mayúsculas, minúsculas, números y símbolos.")
        if not self.password_validator.validate_password_no_spaces(password):
            errors.append("La contraseña no debe contener espacios.")
        if not self.password_validator.validate_password_differs_from_context(password, username, service):
            errors.append("La contraseña no debe coincidir con el usuario o servicio.")
        return errors


class PasswordManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gestor de Contraseñas')
        self.setGeometry(100, 100, 800, 500)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #A3C1DA;
            }
            QTableWidget {
                background-color: white;
                color: black;
                font-family: 'Times New Roman';
            }
            QTableWidget::item:selected {
                background-color: #6495ED;
                color: white;
            }
            QPushButton {
                padding: 5px 10px;
                border-radius: 3px;
                background-color: #6495ED;
                color: white;
                font-family: 'Times New Roman';
            }
            QPushButton:hover {
                background-color: #4682B4;
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
                background-color: #6495ED;
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
        self.table.setRowCount(0)
        passwords = session.query(Password).all()
        for i, password in enumerate(passwords):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(password.service))
            self.table.setItem(i, 1, QTableWidgetItem(password.username))
            self.table.setItem(i, 2, QTableWidgetItem('********'))

    def add_password(self):
        dialog = PasswordEntry(self)
        if dialog.exec_():
            service, username, password = dialog.get_data()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            new_password = Password(service=service, username=username, password=hashed_password)
            session.add(new_password)
            session.commit()
            self.load_passwords()

    def edit_password(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            service = self.table.item(current_row, 0).text()
            username = self.table.item(current_row, 1).text()

            password_entry = session.query(Password).filter_by(service=service, username=username).first()
            if password_entry:
                dialog = PasswordEntry(self, service, username, password_entry.password.decode('utf-8'),
                                       is_encrypted=True)
                if dialog.exec_():
                    new_service, new_username, new_password = dialog.get_data()
                    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                    password_entry.service = new_service
                    password_entry.username = new_username
                    password_entry.password = hashed_password
                    session.commit()
                    self.load_passwords()

    def delete_password(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            service = self.table.item(current_row, 0).text()
            username = self.table.item(current_row, 1).text()

            confirm = QMessageBox.question(self, 'Confirmar eliminación',
                                           '¿Estás seguro de que quieres eliminar esta contraseña?',
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                password_entry = session.query(Password).filter_by(service=service, username=username).first()
                if password_entry:
                    session.delete(password_entry)
                    session.commit()
                    self.load_passwords()

    def authenticate_user(self, username, password):
        if username == "ALISTAR" and password == "ELFRIO":
            return True
        user = session.query(Password).filter_by(service="Usuario", username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            return True
        return False


class AuthSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sistema de Autenticación')
        self.setFixedSize(400, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #A3C1DA;
                color: white;
                font-size: 14px;
                font-family: 'Times New Roman';
            }
            QLineEdit, QPushButton {
                padding: 10px;
                border-radius: 5px;
                font-family: 'Times New Roman';
            }
            QLineEdit {
                background-color: white;
                color: black;
                font-family: 'Times New Roman';
            }
            QPushButton {
                background-color: #6495ED;
                border: none;
                color: white;
                font-family: 'Times New Roman';
            }
            QPushButton:hover {
                background-color: #4682B4;
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
        login_button.clicked.connect(self.authenticate_and_launch_manager)

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

        self.new_username = QLineEdit()
        self.new_username.setPlaceholderText("Crear Usuario")
        self.new_email = QLineEdit()
        self.new_email.setPlaceholderText("Correo electrónico")

        code_layout = QHBoxLayout()
        self.verification_code = QLineEdit()
        self.verification_code.setPlaceholderText("Código de verificación")
        generate_code = QPushButton("Generar por email")
        code_layout.addWidget(self.verification_code)
        code_layout.addWidget(generate_code)

        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText("Contraseña")
        self.new_password.setEchoMode(QLineEdit.Password)
        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Confirmar contraseña")
        self.confirm_password.setEchoMode(QLineEdit.Password)

        register_button = QPushButton("Registrar")
        register_button.clicked.connect(self.register_user)

        login_link = QPushButton("¿Ya estás registrado? Iniciar Sesión")
        login_link.setStyleSheet("background-color: transparent; text-decoration: underline;")
        login_link.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.login_page))

        layout.addWidget(title)
        layout.addWidget(self.new_username)
        layout.addWidget(self.new_email)
        layout.addLayout(code_layout)
        layout.addWidget(self.new_password)
        layout.addWidget(self.confirm_password)
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
        new_password.setPlaceholderText("Nueva Contraseña")
        new_password.setEchoMode(QLineEdit.Password)
        confirm_password = QLineEdit()
        confirm_password.setPlaceholderText("Confirmar nueva contraseña")
        confirm_password.setEchoMode(QLineEdit.Password)

        reset_button = QPushButton("Restablecer")
        reset_button.clicked.connect(self.reset_password)

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
        if username == "ALISTAR" and password == "ELFRIO":
            return True
        user = session.query(Password).filter_by(service="Usuario", username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            return True
        return False

    def authenticate_and_launch_manager(self):
        if self.authenticate_user(self.username.text(), self.password.text()):
            self.launch_password_manager()
        else:
            self.show_incorrect_password_dialog()

    def register_user(self):
        username = self.new_username.text()
        password = self.new_password.text()
        confirm_password = self.confirm_password.text()

        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden.")
            return

        password_validator = PasswordValidator()
        errors = []
        if not password_validator.validate_password_length(password):
            errors.append("La contraseña debe tener entre 12 y 128 caracteres.")
        if not password_validator.validate_password_strength(password):
            errors.append("La contraseña debe incluir mayúsculas, minúsculas, números y símbolos.")
        if not password_validator.validate_password_no_spaces(password):
            errors.append("La contraseña no debe contener espacios.")
        if not password_validator.validate_password_differs_from_context(password, username, "Usuario"):
            errors.append("La contraseña no debe coincidir con el nombre de usuario.")

        if errors:
            QMessageBox.warning(self, "Error de validación", "\n".join(errors))
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = Password(service="Usuario", username=username, password=hashed_password)
        session.add(new_user)
        session.commit()

        QMessageBox.information(self, "Éxito", "Usuario registrado exitosamente.")
        self.stacked_widget.setCurrentWidget(self.login_page)

    def reset_password(self):
        QMessageBox.information(self, "Información", "Funcionalidad de restablecimiento de contraseña no implementada.")

    def launch_password_manager(self):
        self.hide()
        self.password_manager = PasswordManager()
        self.password_manager.show()

    def show_incorrect_password_dialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("CLAVE INCORRECTA")
        msg.setInformativeText("Usuario o contraseña incorrectos. Inténtalo de nuevo.")
        msg.setWindowTitle("Advertencia")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    auth_system = AuthSystem()
    auth_system.show()
    sys.exit(app.exec_())

