"""
Módulo del panel visual donde se generan los reportes estadísticos de morbilidad.
"""

from tkinter import filedialog, messagebox

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from modelos.consultas_medicos import ConsultasMedicos


class PanelReportes(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10, fg_color="transparent")

        self.db = ConsultasMedicos()
        self.canvas_widget = None
        self.fig = None

        self.nombres_meses = [
            "Enero",
            "Febrero",
            "Marzo",
            "Abril",
            "Mayo",
            "Junio",
            "Julio",
            "Agosto",
            "Septiembre",
            "Octubre",
            "Noviembre",
            "Diciembre",
        ]

        self.lbl_titulo = ctk.CTkLabel(
            self, text="Reportes Estadísticos", font=ctk.CTkFont(size=24, weight="bold")
        )
        self.lbl_titulo.pack(pady=(20, 20))

        self.frame_controles = ctk.CTkFrame(self)
        self.frame_controles.pack(pady=10, padx=20, fill="x")

        self.lbl_tipo_periodo = ctk.CTkLabel(
            self.frame_controles, text="Tipo de Reporte:"
        )
        self.lbl_tipo_periodo.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.cmb_tipo_periodo = ctk.CTkComboBox(
            self.frame_controles,
            values=["Mensual", "Trimestral"],
            command=self.actualizar_periodos,
            state="readonly",
        )
        self.cmb_tipo_periodo.grid(row=0, column=1, padx=10, pady=10)
        self.cmb_tipo_periodo.set("Mensual")

        self.lbl_valor_periodo = ctk.CTkLabel(
            self.frame_controles, text="Mes/Trimestre:"
        )
        self.lbl_valor_periodo.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.cmb_valor_periodo = ctk.CTkComboBox(
            self.frame_controles, values=self.nombres_meses, state="readonly"
        )
        self.cmb_valor_periodo.grid(row=0, column=3, padx=10, pady=10)
        self.cmb_valor_periodo.set("Enero")

        self.lbl_anio = ctk.CTkLabel(self.frame_controles, text="Año:")
        self.lbl_anio.grid(row=0, column=4, padx=10, pady=10, sticky="w")

        anios_validos = [str(i) for i in range(1996, 2100)]
        self.cmb_anio = ctk.CTkComboBox(
            self.frame_controles, values=anios_validos, state="readonly", width=100
        )
        self.cmb_anio.grid(row=0, column=5, padx=10, pady=10)
        self.cmb_anio.set("2026")

        self.lbl_tipo_comp = ctk.CTkLabel(self.frame_controles, text="Comparar:")
        self.lbl_tipo_comp.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.cmb_tipo_comp = ctk.CTkComboBox(
            self.frame_controles,
            values=["Médicos por Especialidad", "Especialidades por Grupo"],
            command=self.actualizar_filtros,
            state="readonly",
            width=200,
        )
        self.cmb_tipo_comp.grid(
            row=1, column=1, columnspan=2, padx=10, pady=10, sticky="ew"
        )
        self.cmb_tipo_comp.set("Médicos por Especialidad")

        self.lbl_filtro = ctk.CTkLabel(self.frame_controles, text="Seleccione:")
        self.lbl_filtro.grid(row=1, column=3, padx=10, pady=10, sticky="w")

        self.cmb_filtro = ctk.CTkComboBox(
            self.frame_controles, values=[], state="readonly", width=200
        )
        self.cmb_filtro.grid(
            row=1, column=4, columnspan=2, padx=10, pady=10, sticky="ew"
        )

        self.btn_generar = ctk.CTkButton(
            self.frame_controles,
            text="Generar Gráfico",
            font=ctk.CTkFont(weight="bold"),
            command=self.generar_grafico,
        )
        self.btn_generar.grid(row=2, column=1, columnspan=2, pady=20)

        self.btn_exportar = ctk.CTkButton(
            self.frame_controles,
            text="Exportar Gráfico",
            font=ctk.CTkFont(weight="bold"),
            fg_color="#28a745",
            hover_color="#218838",
            state="disabled",
            command=self.exportar_grafico,
        )
        self.btn_exportar.grid(row=2, column=3, columnspan=2, pady=20)

        self.frame_grafico = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_grafico.pack(pady=10, padx=20, fill="both", expand=True)

        self.actualizar_filtros("Médicos por Especialidad")

    def actualizar_periodos(self, eleccion):
        if eleccion == "Mensual":
            self.cmb_valor_periodo.configure(values=self.nombres_meses)
            self.cmb_valor_periodo.set("Enero")
        else:
            valores = ["Trimestre 1", "Trimestre 2", "Trimestre 3", "Trimestre 4"]
            self.cmb_valor_periodo.configure(values=valores)
            self.cmb_valor_periodo.set("Trimestre 1")

    def actualizar_filtros(self, eleccion):
        if eleccion == "Médicos por Especialidad":
            valores = self.db.obtener_especialidades()
        else:
            valores = self.db.obtener_grupos_profesionales()

        if not valores:
            valores = ["Sin datos"]

        self.cmb_filtro.configure(values=valores)
        self.cmb_filtro.set(valores[0])

    def limpiar_recursos(self):
        """Libera la memoria de Matplotlib y destruye el canvas para evitar errores al cerrar."""
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().destroy()
            self.canvas_widget = None
        self.fig = None
        self.btn_exportar.configure(state="disabled")
        plt.close("all")

    def generar_grafico(self):
        tipo_periodo = self.cmb_tipo_periodo.get()
        seleccion_periodo = self.cmb_valor_periodo.get()
        anio = self.cmb_anio.get()
        tipo_comp = self.cmb_tipo_comp.get()
        filtro = self.cmb_filtro.get()

        if tipo_periodo == "Mensual":
            valor_periodo = self.nombres_meses.index(seleccion_periodo) + 1
        else:
            valor_periodo = int(seleccion_periodo.split(" ")[1])

        if tipo_comp == "Médicos por Especialidad":
            datos = self.db.obtener_reporte_medicos(
                tipo_periodo, valor_periodo, anio, filtro
            )
            titulo = f"Morbilidad en {filtro}\n({seleccion_periodo} - {anio})"
        else:
            datos = self.db.obtener_reporte_especialidades(
                tipo_periodo, valor_periodo, anio, filtro
            )
            titulo = f"Morbilidad de Especialidades ({filtro})\n({seleccion_periodo} - {anio})"

        if not datos:
            messagebox.showinfo(
                "Sin datos",
                "No se encontraron registros de morbilidad para los filtros seleccionados.",
            )
            self.limpiar_recursos()
            return

        self.limpiar_recursos()

        etiquetas = [fila[0] for fila in datos]
        valores = [fila[1] for fila in datos]

        self.fig, ax = plt.subplots(figsize=(6, 4))
        self.fig.patch.set_alpha(0.0)
        ax.pie(valores, labels=etiquetas, autopct="%1.1f%%", startangle=140)
        ax.axis("equal")
        ax.set_title(titulo, pad=20)

        self.canvas_widget = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().pack(fill="both", expand=True)

        self.btn_exportar.configure(state="normal")

    def exportar_grafico(self):
        """Abre un cuadro de diálogo para guardar el gráfico actual como imagen."""
        if self.fig:
            archivo = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("Imagen PNG", "*.png"),
                    ("Imagen JPEG", "*.jpg"),
                    ("Documento PDF", "*.pdf"),
                ],
                title="Guardar Gráfico como...",
            )
            if archivo:
                try:
                    original_alpha = self.fig.patch.get_alpha()

                    self.fig.patch.set_alpha(1.0)
                    self.fig.patch.set_facecolor("white")

                    self.fig.savefig(
                        archivo,
                        bbox_inches="tight",
                        facecolor="white",
                        transparent=False,
                    )

                    self.fig.patch.set_alpha(original_alpha)

                    messagebox.showinfo(
                        "Exportación Exitosa",
                        f"El gráfico se ha guardado correctamente en:\n{archivo}",
                    )
                except Exception as e:
                    if hasattr(self, "fig") and self.fig:
                        self.fig.patch.set_alpha(original_alpha)

                    messagebox.showerror(
                        "Error de Exportación",
                        f"Hubo un problema al guardar el archivo:\n{e}",
                    )
