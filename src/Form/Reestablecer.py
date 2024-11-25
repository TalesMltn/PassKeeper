from tkinter import *
from tkinter import messagebox
from src.database.Reestablecer import DBController

# Crear instancia del controlador de base de datos
db = DBController()

# Ventana del inicio
root = Tk()
root.title('Restablecer Contraseña')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

# Imagen
img = PhotoImage(file='../img/login.png')
Label(root, image=img, bg='#fff').place(x=50, y=50)

# Formulario
frame = Frame(root, width=400, height=400, bg="#fff")
frame.place(x=530, y=70)
heading = Label(frame, text='Restablecer Contraseña', fg='#57a1f8', bg='#fff',
                font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=10, y=5)

# Usuario
def on_enter_user(e):
    user_entry.delete(0, 'end')

def on_leave_user(e):
    if not user_entry.get():
        user_entry.insert(0, 'Usuario')

user_entry = Entry(frame, width=25, fg='black', border=0, bg="#fff", font=('Microsoft YaHei UI Light', 11))
user_entry.place(x=30, y=80)
user_entry.insert(0, 'Usuario')
user_entry.bind('<FocusIn>', on_enter_user)
user_entry.bind('<FocusOut>', on_leave_user)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

# Nueva contraseña
def on_enter_pass(e):
    password_entry.delete(0, 'end')

def on_leave_pass(e):
    if not password_entry.get():
        password_entry.insert(0, 'Nueva Contraseña')

password_entry = Entry(frame, width=25, fg='black', border=0, bg="#fff", font=('Microsoft YaHei UI Light', 11))
password_entry.place(x=30, y=150)
password_entry.insert(0, 'Nueva Contraseña')
password_entry.bind('<FocusIn>', on_enter_pass)
password_entry.bind('<FocusOut>', on_leave_pass)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

# Confirmar contraseña
def on_enter_confirm(e):
    confirm_entry.delete(0, 'end')

def on_leave_confirm(e):
    if not confirm_entry.get():
        confirm_entry.insert(0, 'Confirmar Contraseña')

confirm_entry = Entry(frame, width=25, fg='black', border=0, bg="#fff", font=('Microsoft YaHei UI Light', 11))
confirm_entry.place(x=30, y=215)
confirm_entry.insert(0, 'Confirmar Contraseña')
confirm_entry.bind('<FocusIn>', on_enter_confirm)
confirm_entry.bind('<FocusOut>', on_leave_confirm)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=245)

# Función para restablecer contraseña
def restablecer_contraseña():
    usuario = user_entry.get()
    nueva_contraseña = password_entry.get()
    confirmar_contraseña = confirm_entry.get()

    if not usuario or usuario == 'Usuario':
        messagebox.showerror("Error", "El campo de usuario no puede estar vacío.")
        return
    if nueva_contraseña != confirmar_contraseña:
        messagebox.showerror("Error", "Las contraseñas no coinciden.")
        return

    # Verificar si el usuario existe
    user = db.buscar_usuario(usuario)
    if not user:
        messagebox.showerror("Error", "Usuario no encontrado.")
        return

    # Actualizar la contraseña
    if db.actualizar_contraseña(usuario, nueva_contraseña):
        messagebox.showinfo("Éxito", "Contraseña actualizada correctamente.")
    else:
        messagebox.showerror("Error", "No se pudo actualizar la contraseña.")

# Botón de restablecer
Button(frame, width=39, pady=7, text='Restablecer', bg='#57a1f8', fg='#fff', border=0, command=restablecer_contraseña).place(x=35, y=260)

root.mainloop()
