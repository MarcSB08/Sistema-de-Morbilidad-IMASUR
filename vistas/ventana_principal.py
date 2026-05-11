"""
Ventana principal del sistema, donde se encuentran todas las opciones
"""

import customtkinter as ctk
from vistas.panel_ingreso import PanelIngreso
from vistas.panel_reportes import PanelReportes

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class VentanaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Registro de Morbilidad - IMASUR")

        # Ajusta la ventana a la computadora que se esté utilizando
        try:
            self.after(0, lambda: self.state("zoomed"))
        except:
            try:
                self.attributes("-zoomed", True)
            except:
                ancho = self.winfo_screenwidth()
                alto = self.winfo_screenheight()
                self.geometry(f"{ancho}x{alto}+0+0")

        # Valor mínimo de la ventana
        self.minsize(800, 500)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="IMASUR\nEstadísticas",
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

        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.label_bienvenida = ctk.CTkLabel(
            self.main_frame,
            text="Bienvenido al Sistema de Morbilidad IMASUR",
            font=ctk.CTkFont(size=24),
        )
        self.label_bienvenida.pack(expand=True)

        # Instanciar ambos paneles
        self.panel_ingreso = PanelIngreso(self.main_frame)
        self.panel_reportes = PanelReportes(self.main_frame)

    def mostrar_ingreso(self):
        self.label_bienvenida.pack_forget()
        self.panel_reportes.pack_forget()
        self.panel_ingreso.pack(fill="both", expand=True)
        self.panel_ingreso.limpiar_formulario()

    def mostrar_reportes(self):
        self.label_bienvenida.pack_forget()
        self.panel_ingreso.pack_forget()
        self.panel_reportes.pack(fill="both", expand=True)
