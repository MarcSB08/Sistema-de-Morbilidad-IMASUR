"""
Ventana principal del sistema con logo en la barra lateral.
"""

import customtkinter as ctk
import sys
import os
from PIL import Image
from vistas.panel_ingreso import PanelIngreso
from vistas.panel_reportes import PanelReportes


class VentanaPrincipal(ctk.CTkToplevel):
    def __init__(self, master_window):
        super().__init__(master_window)

        self.master_window = master_window
        self.title("Sistema de Registro de Morbilidad - IMASUR")

        self.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

        try:
            self.after(0, lambda: self.state("zoomed"))
        except:
            ancho = self.winfo_screenwidth()
            alto = self.winfo_screenheight()
            self.geometry(f"{ancho}x{alto}+0+0")

        self.minsize(900, 600)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Barra Lateral
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Cargar Logo para Sidebar
        ruta_base = os.path.dirname(os.path.dirname(__file__))
        ruta_logo = os.path.join(ruta_base, "assets", "logo_imasur.png")

        try:
            img_logo = Image.open(ruta_logo)
            self.logo_image = ctk.CTkImage(
                light_image=img_logo, dark_image=img_logo, size=(80, 80)
            )
            self.logo_label = ctk.CTkLabel(
                self.sidebar_frame, image=self.logo_image, text=""
            )
            self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        except:
            self.logo_label = ctk.CTkLabel(
                self.sidebar_frame,
                text="IMASUR",
                font=ctk.CTkFont(size=20, weight="bold"),
            )
            self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_ingreso = ctk.CTkButton(
            self.sidebar_frame, text="Ingresar Morbilidad", command=self.mostrar_ingreso
        )
        self.btn_ingreso.grid(row=1, column=0, padx=20, pady=10)

        self.btn_reportes = ctk.CTkButton(
            self.sidebar_frame, text="Ver Reportes", command=self.mostrar_reportes
        )
        self.btn_reportes.grid(row=2, column=0, padx=20, pady=10)

        self.btn_logout = ctk.CTkButton(
            self.sidebar_frame,
            text="Cerrar Sesión",
            fg_color="#dc3545",
            hover_color="#c82333",
            command=self.cerrar_sesion,
        )
        self.btn_logout.grid(row=3, column=0, padx=20, pady=10)

        # Frame Principal
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.label_bienvenida = ctk.CTkLabel(
            self.main_frame,
            text="Bienvenido al Sistema de Morbilidad IMASUR",
            font=ctk.CTkFont(size=24),
        )
        self.label_bienvenida.pack(expand=True)

        self.panel_ingreso = PanelIngreso(self.main_frame)
        self.panel_reportes = PanelReportes(self.main_frame)

    def mostrar_ingreso(self):
        self.label_bienvenida.pack_forget()
        self.panel_reportes.pack_forget()
        self.panel_ingreso.pack(fill="both", expand=True)

    def mostrar_reportes(self):
        self.label_bienvenida.pack_forget()
        self.panel_ingreso.pack_forget()
        self.panel_reportes.pack(fill="both", expand=True)

    def cerrar_sesion(self):
        self.panel_reportes.limpiar_recursos()
        self.destroy()
        self.master_window.ent_password.delete(0, "end")
        self.master_window.deiconify()

    def cerrar_aplicacion(self):
        self.panel_reportes.limpiar_recursos()
        self.destroy()
        self.master_window.quit()
        self.master_window.destroy()
        sys.exit()
