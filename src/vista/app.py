import tkinter as tk
from tkinter import ttk, messagebox
from src.modelo.modelo import Usuario
from src.modelo.declarative_base import session, crear_tablas

class UsuarioManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Usuarios")
        self.usuario = None

        # Crear las tablas antes de que la aplicación se ejecute
        crear_tablas()

        # Configuración del frame principal
        self.frame = ttk.Frame(root, padding="20", style="TFrame")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título del formulario
        self.title_label = ttk.Label(self.frame, text="Registrar Usuario", font=("Arial", 18, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))

        # Entradas para registrar usuario
        ttk.Label(self.frame, text="ID:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        self.id_entry = ttk.Entry(self.frame, width=25, font=("Arial", 12))
        self.id_entry.grid(row=1, column=1, sticky=tk.W, pady=5)

        ttk.Label(self.frame, text="Correo:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        self.correo_entry = ttk.Entry(self.frame, width=25, font=("Arial", 12))
        self.correo_entry.grid(row=2, column=1, sticky=tk.W, pady=5)

        ttk.Label(self.frame, text="Contraseña (hash):").grid(row=3, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        self.hash_entry = ttk.Entry(self.frame, width=25, font=("Arial", 12), show="*")
        self.hash_entry.grid(row=3, column=1, sticky=tk.W, pady=5)

        # Botón para registrar usuario
        self.registrar_usuario_btn = ttk.Button(self.frame, text="Registrar Usuario", command=self.registrar_usuario, style="TButton")
        self.registrar_usuario_btn.grid(row=4, column=1, sticky=tk.W, pady=20)

    def registrar_usuario(self):
        # Obtiene los valores de los campos
        id_usuario = self.id_entry.get()

        # Validación del ID como número
        if not id_usuario.isdigit():
            messagebox.showerror("Error", "El ID debe ser un número entero.")
            return

        correo = self.correo_entry.get()  # El correo ya no tiene restricción de caracteres
        hash_contraseña = self.hash_entry.get()

        # Crear el objeto Usuario
        self.usuario = Usuario(
            id=id_usuario,
            correo=correo,
            hash_contraseña=hash_contraseña
        )
        # Guardar el usuario en la base de datos
        session.add(self.usuario)
        session.commit()

        messagebox.showinfo("Éxito", f"Usuario {self.usuario.correo} registrado con éxito.")

# Esta es la parte crítica, debes llamar a mainloop() al final para mostrar la ventana
def run():
    root = tk.Tk()
    app = UsuarioManagerGUI(root)
    root.mainloop()  # Este comando es necesario para que la ventana permanezca abierta

if __name__ == "__main__":
    run()
