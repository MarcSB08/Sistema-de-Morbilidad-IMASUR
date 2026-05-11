"""
Módulo del panel visual donde se generan los reportes estadísticos de morbilidad.
"""

import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from modelos.consultas_medicos import ConsultasMedicos


class PanelReportes(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10, fg_color="transparent")

        self.db = ConsultasMedicos()
        self.canvas_widget = None

        # Lista de meses para facilitar la lectura
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

        # Frame superior para los controles y filtros
        self.frame_controles = ctk.CTkFrame(self)
        self.frame_controles.pack(pady=10, padx=20, fill="x")

        # Fila 0: Controles de Tiempo
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

        # Reemplazamos el Entry por un ComboBox de solo lectura operado con el mouse
        anios_validos = [
            str(i) for i in range(2020, 2041)
        ]  # Años desde 2020 hasta 2040
        self.cmb_anio = ctk.CTkComboBox(
            self.frame_controles, values=anios_validos, state="readonly", width=100
        )
        self.cmb_anio.grid(row=0, column=5, padx=10, pady=10)
        self.cmb_anio.set("2026")  # Año por defecto de tu proyecto

        # Fila 1: Controles de Comparación
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

        # Fila 2: Botón de Generación
        self.btn_generar = ctk.CTkButton(
            self.frame_controles,
            text="Generar Gráfico",
            font=ctk.CTkFont(weight="bold"),
            command=self.generar_grafico,
        )
        self.btn_generar.grid(row=2, column=0, columnspan=6, pady=20)

        # Frame inferior para mostrar el gráfico de Matplotlib
        self.frame_grafico = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_grafico.pack(pady=10, padx=20, fill="both", expand=True)

        # Inicializar los filtros visuales con la base de datos
        self.actualizar_filtros("Médicos por Especialidad")

    def actualizar_periodos(self, eleccion):
        """Cambia las opciones dependiendo si es mes (nombres) o trimestre."""
        if eleccion == "Mensual":
            self.cmb_valor_periodo.configure(values=self.nombres_meses)
            self.cmb_valor_periodo.set("Enero")
        else:
            valores = ["Trimestre 1", "Trimestre 2", "Trimestre 3", "Trimestre 4"]
            self.cmb_valor_periodo.configure(values=valores)
            self.cmb_valor_periodo.set("Trimestre 1")

    def actualizar_filtros(self, eleccion):
        """Carga especialidades o grupos profesionales según lo que se quiera comparar."""
        if eleccion == "Médicos por Especialidad":
            valores = self.db.obtener_especialidades()
        else:
            valores = self.db.obtener_grupos_profesionales()

        if not valores:
            valores = ["Sin datos"]

        self.cmb_filtro.configure(values=valores)
        self.cmb_filtro.set(valores[0])

    def generar_grafico(self):
        """Consulta la base de datos y dibuja el gráfico de torta."""
        tipo_periodo = self.cmb_tipo_periodo.get()
        seleccion_periodo = self.cmb_valor_periodo.get()
        anio = self.cmb_anio.get()
        tipo_comp = self.cmb_tipo_comp.get()
        filtro = self.cmb_filtro.get()

        # Transformar el texto del periodo en el número que requiere la base de datos
        if tipo_periodo == "Mensual":
            # Usamos el índice de la lista (+1 para que coincida con el mes)
            valor_periodo = self.nombres_meses.index(seleccion_periodo) + 1
        else:
            # Extraer solo el número del string "Trimestre X"
            valor_periodo = int(seleccion_periodo.split(" ")[1])

        # Consultar la información estructurada
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
            if self.canvas_widget:
                self.canvas_widget.get_tk_widget().destroy()
                self.canvas_widget = None
            return

        # Separar resultados para el gráfico
        etiquetas = [fila[0] for fila in datos]
        valores = [fila[1] for fila in datos]

        # Limpiar gráfico anterior si existe
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().destroy()

        # Crear figura y gráfico de torta
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_alpha(0.0)  # Fondo transparente para acoplarse al tema de la app
        ax.pie(valores, labels=etiquetas, autopct="%1.1f%%", startangle=140)
        ax.axis("equal")
        ax.set_title(titulo, pad=20)

        # Incrustar en la interfaz de CustomTkinter
        self.canvas_widget = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().pack(fill="both", expand=True)
