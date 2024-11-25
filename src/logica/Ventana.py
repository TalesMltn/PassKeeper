
import subprocess

class Ventana:
    def __init__(self, root):
        self.root = root

    def abrir_passkeeper(self):
        self.root.destroy()
        subprocess.run(["python", "Passkeeper.py"])

    def abrir_reestablecer(self):
        self.root.destroy()
        subprocess.run(["python", "Reestablecer.py"])

    def abrir_registro(self):
        self.root.destroy()
        subprocess.run(["python", "Registro_Usuario.py"])

    def abrir_inicio(self):
            self.root.destroy()
            subprocess.run(["python", "Inicio_Sesion.py"])

