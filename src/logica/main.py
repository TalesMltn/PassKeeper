def registrar_usuario(self):
    try:
        # Obtiene los valores de los campos
        id_usuario = self.id_entry.get()

        # Validación del ID como número
        if not id_usuario.isdigit():
            messagebox.showerror("Error", "El ID debe ser un número entero.")
            return

        # Obtener valores de correo y hash de contraseña
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
    except Exception as e:
        messagebox.showerror("Error desconocido", f"Ocurrió un error inesperado: {e}")
