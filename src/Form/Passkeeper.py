from tkinter import *
from tkinter import ttk
from src.database.tablePasskeeper import obtener_datos_passkeeper

class PasskeeperApp:
    def __init__(self, root, id_usuario):
        self.root = root
        self.id_usuario = id_usuario
        self.root.title('Passkeeper')
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.configure(bg="#fff")
        self.root.resizable(True, True)

        # Contenido principal
        shadow = Frame(self.root, width=350, bg="#d9d9d9")
        shadow.place(x=5, y=5, relheight=1)
        conten = Frame(self.root, width=350, bg="#fff", highlightbackground="#ccc", highlightthickness=1)
        conten.place(x=0, y=0, relheight=1)

        # Imagen
        img = PhotoImage(file='../img/logo.png')
        Label(conten, image=img, bg='#fff').place(x=85, y=35)
        label = Label(conten, text="PassKeeper", fg='Black', bg='#fff', font=('Arial', 20, 'bold'))
        label.place(x=80, y=30)

        agregar = Button(conten, text="AGREGAR", bg='#8E17EB', fg="white", font=("Arial", 10, "bold"), activebackground="#000000", activeforeground="white")
        agregar.place(relx=0, rely=0.15, relwidth=1, height=50)
        config = Button(conten, text="CONFIGURACIÓN", bg='#8E17EB', fg="white", font=("Arial", 10, "bold"), activebackground="#000000", activeforeground="white")
        config.place(relx=0, rely=0.22, relwidth=1, height=50)

        # Tabla
        ftable = Frame(self.root, width=1400, height=800, bg="#fff")
        ftable.place(x=425, y=150, relwidth=0.7, relheight=0.7)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        font=('Arial', 12),
                        rowheight=25,
                        background="#f9f9f9",
                        foreground="#000")
        style.configure("Treeview.Heading",
                        font=('Arial', 12, 'bold'),
                        background="#8E17EB",
                        foreground="white")
        style.map("Treeview",
                  background=[('selected', '#005cbf')],
                  foreground=[('selected', 'black')])

        self.tabla = ttk.Treeview(ftable, columns=("Usuario", "Contraseña", "Sitio WEB", "Seguridad"), show="headings")
        self.tabla.heading("Usuario", text="Usuario")
        self.tabla.heading("Contraseña", text="Contraseña")
        self.tabla.heading("Sitio WEB", text="Sitio WEB")
        self.tabla.heading("Seguridad", text="Seguridad")
        self.tabla.column("Usuario", anchor="center")
        self.tabla.column("Contraseña", anchor="center")
        self.tabla.column("Sitio WEB", anchor="center")
        self.tabla.column("Seguridad", anchor="center")

        scroll_y = ttk.Scrollbar(ftable, orient=VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll_y.set)

        scroll_y.pack(side=RIGHT, fill=Y)
        self.tabla.pack(fill=BOTH, expand=True)

        # Cargar datos
        self.cargar_datos()

        # Mantener referencia de la imagen
        self.img_ref = img

    def cargar_datos(self):
        """
        Carga los datos del usuario actual en la tabla.
        """
        datos = obtener_datos_passkeeper(self.id_usuario)
        for dato in datos:
            self.tabla.insert("", "end", values=dato)

# Para probar la clase
if __name__ == "__main__":
    root = Tk()
    app = PasskeeperApp(root, id_usuario="usuario_prueba")  # Reemplazar con IDUser válido
    root.mainloop()
