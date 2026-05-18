"""
Módulo para visualizar la relación mensual de morbilidad en formato de tabla.
Diseñado para maximizar la visibilidad y separación entre especialidades.
"""

import customtkinter as ctk
from tkinter import ttk, messagebox
from modelos.consultas_medicos import ConsultasMedicos


class PanelRelacion(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10, fg_color="transparent")

        self.db = ConsultasMedicos()
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
            self,
            text="Relación Mensual de Morbilidad",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.lbl_titulo.pack(pady=(20, 10))

        # Controles superiores
        self.frame_controles = ctk.CTkFrame(self)
        self.frame_controles.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(self.frame_controles, text="Mes:").grid(
            row=0, column=0, padx=10, pady=10
        )
        self.cmb_mes = ctk.CTkComboBox(
            self.frame_controles, values=self.nombres_meses, state="readonly"
        )
        self.cmb_mes.grid(row=0, column=1, padx=10, pady=10)
        self.cmb_mes.set("Enero")

        ctk.CTkLabel(self.frame_controles, text="Año:").grid(
            row=0, column=2, padx=10, pady=10
        )
        anios_validos = [str(i) for i in range(2020, 2041)]
        self.cmb_anio = ctk.CTkComboBox(
            self.frame_controles, values=anios_validos, state="readonly", width=100
        )
        self.cmb_anio.grid(row=0, column=3, padx=10, pady=10)
        self.cmb_anio.set("2026")

        self.btn_generar = ctk.CTkButton(
            self.frame_controles,
            text="Generar Tabla",
            font=ctk.CTkFont(weight="bold"),
            command=self.generar_tabla,
        )
        self.btn_generar.grid(row=0, column=4, padx=20, pady=10)

        # Configuración avanzada del estilo de la tabla (Treeview)
        style = ttk.Style()
        style.theme_use("default")

        # Estilo general de las celdas
        style.configure(
            "Treeview",
            background="#2b2b2b",
            foreground="white",
            rowheight=30,
            fieldbackground="#2b2b2b",
            font=("Arial", 10),
        )

        # Estilo de los encabezados principales
        style.configure(
            "Treeview.Heading",
            background="#404040",
            foreground="white",
            font=("Arial", 10, "bold"),
        )

        style.map("Treeview", background=[("selected", "#1f538d")])

        # Frame para la tabla con barras de desplazamiento
        self.frame_tabla = ctk.CTkFrame(self)
        self.frame_tabla.pack(pady=10, padx=20, fill="both", expand=True)

        self.tree_scroll_y = ttk.Scrollbar(self.frame_tabla)
        self.tree_scroll_y.pack(side="right", fill="y")
        self.tree_scroll_x = ttk.Scrollbar(self.frame_tabla, orient="horizontal")
        self.tree_scroll_x.pack(side="bottom", fill="x")

        self.tree = ttk.Treeview(
            self.frame_tabla,
            yscrollcommand=self.tree_scroll_y.set,
            xscrollcommand=self.tree_scroll_x.set,
        )
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)

        # Configuración de etiquetas visuales (Tags) para colores
        self.tree.tag_configure(
            "especialidad_header",
            background="#1f538d",
            foreground="white",
            font=("Arial", 11, "bold"),
        )
        self.tree.tag_configure("par", background="#333333")
        self.tree.tag_configure("impar", background="#2b2b2b")

        # Definir Columnas (1 a 31 + Especialista, Especialidad y Total)
        columnas = (
            ["ESPECIALISTA", "ESPECIALIDAD"]
            + [str(i) for i in range(1, 32)]
            + ["TOTAL"]
        )
        self.tree["columns"] = columnas
        self.tree.column("#0", width=0, stretch=ctk.NO)
        self.tree.heading("#0", text="", anchor=ctk.W)

        self.tree.column("ESPECIALISTA", anchor=ctk.W, width=200)
        self.tree.heading("ESPECIALISTA", text="MÉDICO ESPECIALISTA", anchor=ctk.W)
        self.tree.column("ESPECIALIDAD", anchor=ctk.W, width=180)
        self.tree.heading("ESPECIALIDAD", text="ESPECIALIDAD", anchor=ctk.W)

        for i in range(1, 32):
            self.tree.column(str(i), anchor=ctk.CENTER, width=45)
            self.tree.heading(str(i), text=str(i), anchor=ctk.CENTER)

        self.tree.column("TOTAL", anchor=ctk.CENTER, width=80)
        self.tree.heading("TOTAL", text="TOTAL", anchor=ctk.CENTER)

    def generar_tabla(self):
        mes_texto = self.cmb_mes.get()
        anio = int(self.cmb_anio.get())
        mes_numero = self.nombres_meses.index(mes_texto) + 1

        datos_actuales = self.db.obtener_relacion_mensual(mes_numero, anio)

        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not datos_actuales:
            messagebox.showinfo(
                "Información",
                f"No hay registros de morbilidad para {mes_texto} {anio}.",
            )
            return

        # Insertar datos con formato jerárquico y visual
        for especialidad, medicos in datos_actuales.items():
            # FILA DE SEPARACIÓN: Encabezado de la Especialidad
            self.tree.insert(
                "",
                ctk.END,
                values=(especialidad.upper(), "", *[""] * 31, ""),
                tags=("especialidad_header",),
            )

            # FILAS DE MÉDICOS: Alternando colores para visibilidad
            for idx, (medico, dias) in enumerate(medicos.items()):
                tag = "par" if idx % 2 == 0 else "impar"

                # Preparamos los valores de la fila
                valores = [medico, especialidad]
                for i in range(1, 32):
                    # Dejamos la celda vacía si es 0 para que resalten más los números reales (opcional)
                    valor_dia = dias[i] if dias[i] > 0 else ""
                    valores.append(valor_dia)

                valores.append(dias["total"])

                self.tree.insert("", ctk.END, values=valores, tags=(tag,))

            # Insertar una fila vacía pequeña de separación extra entre bloques
            self.tree.insert("", ctk.END, values=("", "", *[""] * 31, ""))
