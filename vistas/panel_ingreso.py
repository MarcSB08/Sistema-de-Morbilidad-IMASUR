"""
Módulo del panel visual donde se registra la fecha, el médico
especialista y los pacientes atendidos por este.
"""

import datetime
from tkinter import messagebox

import customtkinter as ctk
from tkcalendar import Calendar

from modelos.consultas_medicos import ConsultasMedicos


class PanelIngreso(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10, fg_color="transparent")

        self.db = ConsultasMedicos()

        self.lbl_titulo = ctk.CTkLabel(
            self,
            text="Registro Diario de Morbilidad",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.lbl_titulo.pack(pady=(20, 30))

        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(pady=10, padx=50, fill="both", expand=True)
        self.form_frame.grid_columnconfigure(1, weight=1)

        self.lbl_fecha = ctk.CTkLabel(
            self.form_frame, text="Fecha:", font=ctk.CTkFont(size=14)
        )
        self.lbl_fecha.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.frame_fecha = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.frame_fecha.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
        self.frame_fecha.grid_columnconfigure(0, weight=1)

        self.ent_fecha = ctk.CTkEntry(
            self.frame_fecha,
            placeholder_text="Presione el botón azul para seleccionar una fecha",
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

        self.lbl_cantidad = ctk.CTkLabel(
            self.form_frame, text="Pacientes Atendidos:", font=ctk.CTkFont(size=14)
        )
        self.lbl_cantidad.grid(row=3, column=0, padx=20, pady=20, sticky="w")

        validacion = (self.register(self.validar_numeros), "%P")
        self.ent_cantidad = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Ej: 15",
            height=35,
            validate="key",
            validatecommand=validacion,
        )
        self.ent_cantidad.grid(row=3, column=1, padx=20, pady=20, sticky="ew")

        # Frame para agrupar botones de acción
        self.frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botones.pack(pady=(20, 40))

        self.btn_guardar = ctk.CTkButton(
            self.frame_botones,
            text="Guardar / Actualizar",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=45,
            fg_color="#28a745",
            hover_color="#218838",
            command=self.guardar_datos,
        )
        self.btn_guardar.grid(row=0, column=0, padx=15)

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

    def validar_numeros(self, texto):
        if texto == "" or texto.isdigit():
            return True
        return False

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
            mindate=datetime.date(1996, 1, 1),
            maxdate=datetime.date(2099, 12, 31),
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

    def guardar_datos(self):
        fecha = self.ent_fecha.get()
        especialidad = self.cmb_especialidad.get()
        medico = self.cmb_medico.get()
        cantidad = self.ent_cantidad.get()

        errores = []
        if not fecha:
            errores.append("Debe seleccionar una fecha.")
        else:
            try:
                # Validar que el año se encuentre en el rango correcto
                anio_seleccionado = int(fecha.split("-")[0])
                if not (1996 <= anio_seleccionado <= 2099):
                    errores.append(
                        "El año del registro debe estar comprendido entre 1996 y 2099."
                    )
            except ValueError:
                pass

        if especialidad == "Seleccione una especialidad..." or not especialidad:
            errores.append("Debe seleccionar una especialidad válida.")
        if (
            medico == "Seleccione un especialista..."
            or medico == "No hay médicos registrados"
            or not medico
        ):
            errores.append("Debe seleccionar un médico válido.")
        if not cantidad:
            errores.append("Debe ingresar la cantidad de pacientes.")

        if errores:
            messagebox.showerror("Campos Incompletos", "\n".join(errores))
            return

        # Validación de duplicidad
        existe, cantidad_actual = self.db.verificar_registro_existente(fecha, medico)

        if existe:
            respuesta = messagebox.askyesno(
                "Registro Existente",
                f"Ya existe un registro para {medico} el día {fecha} con {cantidad_actual} pacientes.\n\n¿Desea actualizarlo al nuevo valor introducido ({cantidad})?",
            )
            if respuesta:
                exito = self.db.actualizar_registro_morbilidad(
                    fecha, medico, int(cantidad)
                )
                if exito:
                    messagebox.showinfo(
                        "Actualización Exitosa",
                        "El registro ha sido actualizado correctamente.",
                    )
                    self.limpiar_formulario()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el registro.")
            return

        exito = self.db.guardar_registro_morbilidad(fecha, medico, int(cantidad))

        if exito:
            messagebox.showinfo(
                "Registro Exitoso", f"La morbilidad de {medico} ha sido registrada."
            )
            self.limpiar_formulario()
        else:
            messagebox.showerror(
                "Error de Conexión",
                "Hubo un problema al guardar el registro en la base de datos.",
            )

    def limpiar_formulario(self):
        self.ent_fecha.delete(0, "end")
        self.cmb_especialidad.set("Seleccione una especialidad...")
        self.cmb_medico.configure(values=["Seleccione un especialista..."])
        self.cmb_medico.set("Seleccione un especialista...")
        self.ent_cantidad.delete(0, "end")
        self.focus_set()
