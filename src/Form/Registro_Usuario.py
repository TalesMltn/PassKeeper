from tkinter import *
from tkinter import messagebox
from src.database.Registro import registrar_usuario_bd
from src.Logica.Ventana import Ventana



def registrar_usuario():
    correo = email.get()
    nombre = user.get()
    contrasena = password.get()
    confirmar_contrasena = confirm.get()

    # Validación del formulario
    if not correo or correo == 'Correo Electronico':
        messagebox.showerror("Error", "Por favor ingresa un correo válido.")
        return
    if not nombre or nombre == 'Usuario':
        messagebox.showerror("Error", "Por favor ingresa un nombre de usuario.")
        return
    if not contrasena or contrasena == 'Contraseña':
        messagebox.showerror("Error", "Por favor ingresa una contraseña.")
        return
    if contrasena != confirmar_contrasena:
        messagebox.showerror("Error", "Las contraseñas no coinciden.")
        return

    # Intentar registrar al usuario en la base de datos
    if registrar_usuario_bd(nombre, contrasena, correo):
        messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
        limpiar_formulario()

# Función para limpiar el formulario después de registrar
def limpiar_formulario():
    email.delete(0, END)
    email.insert(0, 'Correo Electronico')
    user.delete(0, END)
    user.insert(0, 'Usuario')
    password.delete(0, END)
    password.insert(0, 'Contraseña')
    confirm.delete(0, END)
    confirm.insert(0, 'Confirmar Contraseña')

# Ventana del inicio
root = Tk()
root.title('Registro de Usuario')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)
app_manager = Ventana(root)
# Imagen
img = PhotoImage(file='../img/login.png')
Label(root, image=img, bg='#fff').place(x=50, y=50)

# Formulario
frame = Frame(root, width=350, height=380, bg="white")
frame.place(x=480, y=70)
heading = Label(frame, text='Registrar Usuario', fg='#57a1f8', bg='#fff', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=60, y=5)

# Funciones de ayuda para los campos
def on_enter_email(e):
    if email.get() == 'Correo Electronico':
        email.delete(0, 'end')

def on_leave_email(e):
    if email.get() == '':
        email.insert(0, 'Correo Electronico')

def on_enter_user(e):
    if user.get() == 'Usuario':
        user.delete(0, 'end')

def on_leave_user(e):
    if user.get() == '':
        user.insert(0, 'Usuario')

def on_enter_password(e):
    if password.get() == 'Contraseña':
        password.delete(0, 'end')

def on_leave_password(e):
    if password.get() == '':
        password.insert(0, 'Contraseña')

def on_enter_confirm(e):
    if confirm.get() == 'Confirmar Contraseña':
        confirm.delete(0, 'end')

def on_leave_confirm(e):
    if confirm.get() == '':
        confirm.insert(0, 'Confirmar Contraseña')

# Campos del formulario
email = Entry(frame, width=25, fg='black', border=0, bg="#fff", font=('Microsoft YaHei UI Light', 11))
email.place(x=30, y=80)
email.insert(0, 'Correo Electronico')
email.bind('<FocusIn>', on_enter_email)
email.bind('<FocusOut>', on_leave_email)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

user = Entry(frame, width=25, fg='black', border=0, bg="#fff", font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=125)
user.insert(0, 'Usuario')
user.bind('<FocusIn>', on_enter_user)
user.bind('<FocusOut>', on_leave_user)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=153)

password = Entry(frame, width=25, fg='black', border=0, bg="#fff", font=('Microsoft YaHei UI Light', 11))
password.place(x=30, y=170)
password.insert(0, 'Contraseña')
password.bind('<FocusIn>', on_enter_password)
password.bind('<FocusOut>', on_leave_password)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=198)

confirm = Entry(frame, width=25, fg='black', border=0, bg="#fff", font=('Microsoft YaHei UI Light', 11))
confirm.place(x=30, y=215)
confirm.insert(0, 'Confirmar Contraseña')
confirm.bind('<FocusIn>', on_enter_confirm)
confirm.bind('<FocusOut>', on_leave_confirm)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=245)

# Botón para registrar
Button(frame, width=39, pady=7, text='Registrar', bg='#57a1f8', fg='#fff', border=0, command=registrar_usuario).place(x=35, y=260)

label = Label(frame, text="¿Ya tienes una cuenta?", fg='black', bg='#fff', font=('Microsoft YaHei UI Light', 9))
label.place(x=80, y=305)

sign = Button(frame, width=10, text="Iniciar Sesion", border=0, bg='#fff', cursor='hand2', fg='#57a1f8',command=app_manager.abrir_inicio)
sign.place(x=215, y=305)

root.mainloop()
