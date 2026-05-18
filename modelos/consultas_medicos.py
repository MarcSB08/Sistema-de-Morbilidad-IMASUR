"""
Módulo que maneja las consultas a la base de datos relacionadas con los médicos,
la morbilidad y la validación de usuarios.
"""

from modelos.conexion_db import ConexionDB


class ConsultasMedicos:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def obtener_especialidades(self):
        """Extrae la lista de especialidades médicas desde la base de datos."""
        conexion = self.conexion_db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT nombre FROM especialidades ORDER BY nombre ASC")
                resultados = cursor.fetchall()
                return [fila[0] for fila in resultados]
            except Exception as e:
                print(f"Error al consultar especialidades: {e}")
                return []
            finally:
                self.conexion_db.desconectar(conexion)
        return []

    def obtener_medicos_por_especialidad(self, nombre_especialidad):
        """Extrae los médicos filtrados por la especialidad seleccionada."""
        conexion = self.conexion_db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                consulta = """
                    SELECT m.nombre_medico 
                    FROM medicos m
                    JOIN especialidades e ON m.id_especialidad = e.id_especialidad
                    WHERE e.nombre = %s
                    ORDER BY m.nombre_medico ASC
                """
                cursor.execute(consulta, (nombre_especialidad,))
                resultados = cursor.fetchall()
                return [fila[0] for fila in resultados]
            except Exception as e:
                print(f"Error al consultar médicos: {e}")
                return []
            finally:
                self.conexion_db.desconectar(conexion)
        return []

    def guardar_registro_morbilidad(self, fecha, nombre_medico, cantidad_pacientes):
        """Guarda el registro de morbilidad diaria en la base de datos."""
        conexion = self.conexion_db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                consulta_id = "SELECT id_medico FROM medicos WHERE nombre_medico = %s"
                cursor.execute(consulta_id, (nombre_medico,))
                resultado = cursor.fetchone()

                if resultado:
                    id_medico = resultado[0]
                    consulta_insert = """
                        INSERT INTO morbilidad_diaria (fecha, id_medico, cantidad_pacientes)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(
                        consulta_insert, (fecha, id_medico, cantidad_pacientes)
                    )
                    conexion.commit()
                    return True
                else:
                    print("Médico no encontrado en la base de datos.")
                    return False

            except Exception as e:
                print(f"Error al guardar el registro de morbilidad: {e}")
                conexion.rollback()
                return False
            finally:
                self.conexion_db.desconectar(conexion)
        return False

    def obtener_grupos_profesionales(self):
        """Extrae la lista de grupos profesionales únicos desde la base de datos."""
        conexion = self.conexion_db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    "SELECT DISTINCT grupo_profesional FROM especialidades ORDER BY grupo_profesional ASC"
                )
                resultados = cursor.fetchall()
                return [fila[0] for fila in resultados]
            except Exception as e:
                print(f"Error al consultar grupos profesionales: {e}")
                return []
            finally:
                self.conexion_db.desconectar(conexion)
        return []

    def obtener_reporte_medicos(self, tipo_periodo, valor_periodo, anio, especialidad):
        """Calcula la morbilidad total por médico dentro de una especialidad en un periodo."""
        conexion = self.conexion_db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                if tipo_periodo == "Mensual":
                    filtro_tiempo = "MONTH(md.fecha) = %s"
                else:
                    filtro_tiempo = "QUARTER(md.fecha) = %s"

                consulta = f"""
                    SELECT m.nombre_medico, SUM(md.cantidad_pacientes) as total
                    FROM morbilidad_diaria md
                    JOIN medicos m ON md.id_medico = m.id_medico
                    JOIN especialidades e ON m.id_especialidad = e.id_especialidad
                    WHERE {filtro_tiempo} AND YEAR(md.fecha) = %s AND e.nombre = %s
                    GROUP BY m.id_medico
                    ORDER BY total DESC
                """
                cursor.execute(consulta, (valor_periodo, anio, especialidad))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al generar reporte de médicos: {e}")
                return []
            finally:
                self.conexion_db.desconectar(conexion)
        return []

    def obtener_reporte_especialidades(
        self, tipo_periodo, valor_periodo, anio, grupo_profesional
    ):
        """Calcula la morbilidad total por especialidad dentro de un grupo profesional en un periodo."""
        conexion = self.conexion_db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                if tipo_periodo == "Mensual":
                    filtro_tiempo = "MONTH(md.fecha) = %s"
                else:
                    filtro_tiempo = "QUARTER(md.fecha) = %s"

                consulta = f"""
                    SELECT e.nombre, SUM(md.cantidad_pacientes) as total
                    FROM morbilidad_diaria md
                    JOIN medicos m ON md.id_medico = m.id_medico
                    JOIN especialidades e ON m.id_especialidad = e.id_especialidad
                    WHERE {filtro_tiempo} AND YEAR(md.fecha) = %s AND e.grupo_profesional = %s
                    GROUP BY e.id_especialidad
                    ORDER BY total DESC
                """
                cursor.execute(consulta, (valor_periodo, anio, grupo_profesional))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al generar reporte de especialidades: {e}")
                return []
            finally:
                self.conexion_db.desconectar(conexion)
        return []

    def validar_usuario(self, usuario, password):
        """Verifica si las credenciales coinciden con un usuario en la base de datos."""
        conexion = self.conexion_db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                consulta = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND contrasena = %s"
                cursor.execute(consulta, (usuario, password))
                resultado = cursor.fetchone()
                return resultado is not None
            except Exception as e:
                print(f"Error al validar usuario: {e}")
                return False
            finally:
                self.conexion_db.desconectar(conexion)
        return False

    def obtener_relacion_mensual(self, mes, anio):
        """Genera la tabla cruzada de morbilidad diaria por médico para un mes y año específico."""
        conexion = self.conexion_db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                consulta = """
                    SELECT e.nombre AS especialidad, m.nombre_medico, DAY(md.fecha) AS dia, SUM(md.cantidad_pacientes) as total_dia
                    FROM medicos m
                    JOIN especialidades e ON m.id_especialidad = e.id_especialidad
                    LEFT JOIN morbilidad_diaria md ON m.id_medico = md.id_medico 
                        AND MONTH(md.fecha) = %s AND YEAR(md.fecha) = %s
                    GROUP BY e.nombre, m.nombre_medico, DAY(md.fecha)
                    ORDER BY e.nombre ASC, m.nombre_medico ASC
                """
                cursor.execute(consulta, (mes, anio))
                resultados = cursor.fetchall()

                datos_procesados = {}
                for especialidad, medico, dia, total_dia in resultados:
                    if especialidad not in datos_procesados:
                        datos_procesados[especialidad] = {}
                    if medico not in datos_procesados[especialidad]:
                        datos_procesados[especialidad][medico] = {
                            d: 0 for d in range(1, 32)
                        }
                        datos_procesados[especialidad][medico]["total"] = 0

                    if dia is not None:
                        datos_procesados[especialidad][medico][dia] = int(total_dia)
                        datos_procesados[especialidad][medico]["total"] += int(
                            total_dia
                        )

                return datos_procesados
            except Exception as e:
                print(f"Error al generar relación mensual: {e}")
                return {}
            finally:
                self.conexion_db.desconectar(conexion)
        return {}
