"""
Módulo encargado de la interfaz de inicio de sesión del sistema.
"""

import customtkinter as ctk
from tkinter import messagebox


class Login(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Inicio de Sesión - IMASUR")
        self.geometry("400x500")
        self.resizable(False, False)

        # Centrar la ventana en la pantalla
        ancho_ventana = 400
        alto_ventana = 500
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        self.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        # Configuración de diseño
        self.grid_columnconfigure(0, weight=1)

        self.lbl_logo = ctk.CTkLabel(
            self, text="IMASUR\nEstadísticas", font=ctk.CTkFont(size=30, weight="bold")
        )
        self.lbl_logo.grid(row=0, column=0, pady=(50, 30))

        self.frame_login = ctk.CTkFrame(self, corner_radius=15)
        self.frame_login.grid(row=1, column=0, padx=40, pady=10, sticky="nsew")
        self.frame_login.grid_columnconfigure(0, weight=1)

        self.lbl_bienvenida = ctk.CTkLabel(
            self.frame_login,
            text="Bienvenido",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.lbl_bienvenida.grid(row=0, column=0, pady=(20, 20))

        # Campo de Usuario
        self.ent_usuario = ctk.CTkEntry(
            self.frame_login, placeholder_text="Usuario", height=45, width=280
        )
        self.ent_usuario.grid(row=1, column=0, pady=10)

        # Campo de Contraseña
        self.ent_password = ctk.CTkEntry(
            self.frame_login,
            placeholder_text="Contraseña",
            show="*",
            height=45,
            width=280,
        )
        self.ent_password.grid(row=2, column=0, pady=10)

        # Botón de Ingreso
        self.btn_login = ctk.CTkButton(
            self.frame_login,
            text="Iniciar Sesión",
            height=45,
            width=280,
            font=ctk.CTkFont(weight="bold"),
            command=self.validar_acceso,
        )
        self.btn_login.grid(row=3, column=0, pady=(30, 40))

    def validar_acceso(self):
        usuario = self.ent_usuario.get()
        password = self.ent_password.get()

        # Credenciales solicitadas
        if usuario == "admin" and password == "123456":
            self.destroy()  # Cerramos la ventana de login
            from vistas.ventana_principal import VentanaPrincipal

            app_principal = VentanaPrincipal()
            app_principal.mainloop()
        else:
            messagebox.showerror(
                "Acceso Denegado",
                "El usuario o la contraseña son incorrectos. Por favor, intente de nuevo.",
            )
