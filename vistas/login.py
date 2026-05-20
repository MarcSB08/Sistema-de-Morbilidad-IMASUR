"""
Módulo encargado de la interfaz de inicio de sesión del sistema.
"""

import customtkinter as ctk
from tkinter import messagebox
from modelos.consultas_medicos import ConsultasMedicos
from PIL import Image
import os


class Login(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db = ConsultasMedicos()

        self.title("Inicio de Sesión - IMASUR")
        self.geometry("400x550")
        self.resizable(False, False)

        ancho_ventana = 400
        alto_ventana = 550
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        self.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        self.grid_columnconfigure(0, weight=1)

        ruta_base = os.path.dirname(os.path.dirname(__file__))
        ruta_logo = os.path.join(ruta_base, "assets", "logo_imasur.png")

        try:
            img_logo = Image.open(ruta_logo)
            self.logo_image = ctk.CTkImage(
                light_image=img_logo, dark_image=img_logo, size=(120, 120)
            )

            self.lbl_logo = ctk.CTkLabel(self, image=self.logo_image, text="")
            self.lbl_logo.grid(row=0, column=0, pady=(40, 10))
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")
            self.lbl_logo = ctk.CTkLabel(
                self, text="IMASUR", font=ctk.CTkFont(size=30, weight="bold")
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

        self.ent_usuario = ctk.CTkEntry(
            self.frame_login, placeholder_text="Usuario", height=45, width=280
        )
        self.ent_usuario.grid(row=1, column=0, pady=10)

        self.ent_password = ctk.CTkEntry(
            self.frame_login,
            placeholder_text="Contraseña",
            show="*",
            height=45,
            width=280,
        )
        self.ent_password.grid(row=2, column=0, pady=10)

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

        if self.db.validar_usuario(usuario, password):
            self.withdraw()
            from vistas.ventana_principal import VentanaPrincipal

            app_principal = VentanaPrincipal(self)
        else:
            messagebox.showerror("Acceso Denegado", "Usuario o contraseña incorrectos.")
