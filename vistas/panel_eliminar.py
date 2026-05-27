"""
Módulo del panel visual dedicado a eliminar registros estadísticos de morbilidad.
"""

import customtkinter as ctk
from tkcalendar import Calendar
from tkinter import messagebox
from modelos.consultas_medicos import ConsultasMedicos


class PanelEliminar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10, fg_color="transparent")

        self.db = ConsultasMedicos()

        self.lbl_titulo = ctk.CTkLabel(
            self,
            text="Eliminar Registro de Morbilidad",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.lbl_titulo.pack(pady=(20, 30))

        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(pady=10, padx=50, fill="both", expand=True)
        self.form_frame.grid_columnconfigure(1, weight=1)

        self.lbl_fecha = ctk.CTkLabel(
            self.form_frame, text="Fecha del Registro:", font=ctk.CTkFont(size=14)
        )
        self.lbl_fecha.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.frame_fecha = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.frame_fecha.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
        self.frame_fecha.grid_columnconfigure(0, weight=1)

        self.ent_fecha = ctk.CTkEntry(
            self.frame_fecha,
            placeholder_text="Seleccione la fecha a buscar",
            height=35,
        )
        self.ent_fecha.grid(row=0, column=0, sticky="ew")
        self.ent_fecha.bind("<Key>", lambda e: "break")
        self.ent_fecha.bind("<Button-1>", lambda e: self.focus_set())

        self.btn_calendario = ctk.CTkButton(
            self.frame_fecha,
            text="...",
            width=40,
            height=35,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.abrir_calendario,
        )
        self.btn_calendario.grid(row=0, column=1, padx=(10, 0))

        self.lbl_especialidad = ctk.CTkLabel(
            self.form_frame, text="Especialidad:", font=ctk.CTkFont(size=14)
        )
        self.lbl_especialidad.grid(row=1, column=0, padx=20, pady=20, sticky="w")

        self.cmb_especialidad = ctk.CTkComboBox(
            self.form_frame,
            values=["Seleccione una especialidad..."],
            height=35,
            state="readonly",
            command=self.actualizar_medicos,
        )
        self.cmb_especialidad.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

        self.lbl_medico = ctk.CTkLabel(
            self.form_frame, text="Médico Especialista:", font=ctk.CTkFont(size=14)
        )
        self.lbl_medico.grid(row=2, column=0, padx=20, pady=20, sticky="w")

        self.cmb_medico = ctk.CTkComboBox(
            self.form_frame,
            values=["Seleccione un especialista..."],
            height=35,
            state="readonly",
        )
        self.cmb_medico.grid(row=2, column=1, padx=20, pady=20, sticky="ew")

        self.btn_eliminar = ctk.CTkButton(
            self,
            text="Buscar y Eliminar",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            fg_color="#dc3545",
            hover_color="#c82333",
            command=self.eliminar_datos,
        )
        self.btn_eliminar.pack(pady=(20, 40))

        self.cargar_especialidades()
        self.after(100, self.focus_set)

    def cargar_especialidades(self):
        especialidades = self.db.obtener_especialidades()
        valores = ["Seleccione una especialidad..."] + especialidades
        self.cmb_especialidad.configure(values=valores)
        self.cmb_especialidad.set("Seleccione una especialidad...")

    def actualizar_medicos(self, especialidad_seleccionada):
        if especialidad_seleccionada == "Seleccione una especialidad...":
            self.cmb_medico.configure(values=["Seleccione un especialista..."])
            self.cmb_medico.set("Seleccione un especialista...")
            return

        medicos = self.db.obtener_medicos_por_especialidad(especialidad_seleccionada)

        if medicos:
            valores = ["Seleccione un especialista..."] + medicos
        else:
            valores = ["Seleccione un especialista...", "No hay médicos registrados"]

        self.cmb_medico.configure(values=valores)
        self.cmb_medico.set("Seleccione un especialista...")

    def abrir_calendario(self):
        ventana_cal = ctk.CTkToplevel(self)
        ventana_cal.title("Seleccionar Fecha")
        ventana_cal.geometry("300x300")
        ventana_cal.attributes("-topmost", True)

        ventana_cal.wait_visibility()
        ventana_cal.grab_set()

        cal = Calendar(
            ventana_cal,
            selectmode="day",
            date_pattern="yyyy-mm-dd",
            showweeknumbers=False,
        )
        cal.pack(pady=20, padx=20, fill="both", expand=True)

        def seleccionar_fecha():
            self.ent_fecha.delete(0, "end")
            self.ent_fecha.insert(0, cal.get_date())
            ventana_cal.destroy()

        btn_confirmar = ctk.CTkButton(
            ventana_cal, text="Aceptar", command=seleccionar_fecha
        )
        btn_confirmar.pack(pady=(0, 20))

    def eliminar_datos(self):
        fecha = self.ent_fecha.get()
        medico = self.cmb_medico.get()

        errores = []
        if not fecha:
            errores.append("Debe seleccionar una fecha.")
        if (
            medico == "Seleccione un especialista..."
            or medico == "No hay médicos registrados"
            or not medico
        ):
            errores.append("Debe seleccionar un médico válido.")

        if errores:
            messagebox.showerror("Campos Incompletos", "\n".join(errores))
            return

        # Verificar si hay un registro guardado en esa fecha para ese médico
        existe, cantidad_actual = self.db.verificar_registro_existente(fecha, medico)

        if not existe:
            messagebox.showwarning(
                "Registro No Encontrado",
                f"No se encontró ningún registro estadístico para {medico} en la fecha {fecha}.",
            )
            return

        # Confirmación de la eliminación
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"Se ha encontrado el registro de {medico} para el {fecha}.\n"
            f"Pacientes atendidos registrados: {cantidad_actual}\n\n"
            f"¿Está seguro que desea eliminar este registro permanentemente?",
        )

        if respuesta:
            exito = self.db.eliminar_registro_morbilidad(fecha, medico)
            if exito:
                messagebox.showinfo(
                    "Eliminación Exitosa",
                    "El registro ha sido eliminado correctamente del sistema.",
                )
                self.limpiar_formulario()
            else:
                messagebox.showerror(
                    "Error",
                    "Ocurrió un problema de conexión y no se pudo eliminar el registro.",
                )

    def limpiar_formulario(self):
        self.ent_fecha.delete(0, "end")
        self.cmb_especialidad.set("Seleccione una especialidad...")
        self.cmb_medico.configure(values=["Seleccione un especialista..."])
        self.cmb_medico.set("Seleccione un especialista...")
        self.focus_set()
