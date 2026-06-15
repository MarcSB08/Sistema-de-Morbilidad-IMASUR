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
                    WHERE e.nombre = ?
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

    def verificar_registro_existente(self, fecha, nombre_medico):
        """Verifica si ya existe un registro para un médico en una fecha específica y devuelve su cantidad."""
        conexion = self.conexion_db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                consulta = """
                    SELECT md.cantidad_pacientes
                    FROM morbilidad_diaria md
                    JOIN medicos m ON md.id_medico = m.id_medico
                    WHERE md.fecha = ? AND m.nombre_medico = ?
                """
                cursor.execute(consulta, (fecha, nombre_medico))
                resultado = cursor.fetchone()
                if resultado:
                    return True, resultado[0]
                return False, 0
            except Exception as e:
                print(f"Error al verificar registro: {e}")
                return False, 0
            finally:
                self.conexion_db.desconectar(conexion)
        return False, 0

    def guardar_registro_morbilidad(self, fecha, nombre_medico, cantidad_pacientes):
        """Guarda un nuevo registro de morbilidad diaria en la base de datos."""
        conexion = self.conexion_db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                consulta_id = "SELECT id_medico FROM medicos WHERE nombre_medico = ?"
                cursor.execute(consulta_id, (nombre_medico,))
                resultado = cursor.fetchone()

                if resultado:
                    id_medico = resultado[0]
                    consulta_insert = """
                        INSERT INTO morbilidad_diaria (fecha, id_medico, cantidad_pacientes)
                        VALUES (?, ?, ?)
                    """
                    cursor.execute(
                        consulta_insert, (fecha, id_medico, cantidad_pacientes)
                    )
                    conexion.commit()
                    return True
                else:
                    return False
            except Exception as e:
                print(f"Error al guardar el registro de morbilidad: {e}")
                conexion.rollback()
                return False
            finally:
                self.conexion_db.desconectar(conexion)
        return False

    def actualizar_registro_morbilidad(self, fecha, nombre_medico, cantidad_pacientes):
        """Actualiza la cantidad de pacientes de un registro de morbilidad existente."""
        conexion = self.conexion_db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                consulta_id = "SELECT id_medico FROM medicos WHERE nombre_medico = ?"
                cursor.execute(consulta_id, (nombre_medico,))
                resultado = cursor.fetchone()

                if resultado:
                    id_medico = resultado[0]
                    consulta_update = """
                        UPDATE morbilidad_diaria
                        SET cantidad_pacientes = ?
                        WHERE fecha = ? AND id_medico = ?
                    """
                    cursor.execute(
                        consulta_update, (cantidad_pacientes, fecha, id_medico)
                    )
                    conexion.commit()
                    return True
                return False
            except Exception as e:
                print(f"Error al actualizar el registro: {e}")
                conexion.rollback()
                return False
            finally:
                self.conexion_db.desconectar(conexion)
        return False

    def eliminar_registro_morbilidad(self, fecha, nombre_medico):
        """Elimina un registro de morbilidad específico de la base de datos."""
        conexion = self.conexion_db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                consulta_id = "SELECT id_medico FROM medicos WHERE nombre_medico = ?"
                cursor.execute(consulta_id, (nombre_medico,))
                resultado = cursor.fetchone()

                if resultado:
                    id_medico = resultado[0]
                    consulta_delete = "DELETE FROM morbilidad_diaria WHERE fecha = ? AND id_medico = ?"
                    cursor.execute(consulta_delete, (fecha, id_medico))
                    conexion.commit()
                    return cursor.rowcount > 0
                return False
            except Exception as e:
                print(f"Error al eliminar el registro: {e}")
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
                    filtro_tiempo = "CAST(strftime('%m', md.fecha) AS INTEGER) = ?"
                else:
                    filtro_tiempo = (
                        "((CAST(strftime('%m', md.fecha) AS INTEGER) + 2) / 3) = ?"
                    )

                consulta = f"""
                    SELECT m.nombre_medico, SUM(md.cantidad_pacientes) as total
                    FROM morbilidad_diaria md
                    JOIN medicos m ON md.id_medico = m.id_medico
                    JOIN especialidades e ON m.id_especialidad = e.id_especialidad
                    WHERE {filtro_tiempo} AND CAST(strftime('%Y', md.fecha) AS INTEGER) = ? AND e.nombre = ?
                    GROUP BY m.id_medico
                    ORDER BY total DESC
                """
                cursor.execute(consulta, (int(valor_periodo), int(anio), especialidad))
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
                    filtro_tiempo = "CAST(strftime('%m', md.fecha) AS INTEGER) = ?"
                else:
                    filtro_tiempo = (
                        "((CAST(strftime('%m', md.fecha) AS INTEGER) + 2) / 3) = ?"
                    )

                consulta = f"""
                    SELECT e.nombre, SUM(md.cantidad_pacientes) as total
                    FROM morbilidad_diaria md
                    JOIN medicos m ON md.id_medico = m.id_medico
                    JOIN especialidades e ON m.id_especialidad = e.id_especialidad
                    WHERE {filtro_tiempo} AND CAST(strftime('%Y', md.fecha) AS INTEGER) = ? AND e.grupo_profesional = ?
                    GROUP BY e.id_especialidad
                    ORDER BY total DESC
                """
                cursor.execute(
                    consulta, (int(valor_periodo), int(anio), grupo_profesional)
                )
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
                consulta = (
                    "SELECT * FROM usuarios WHERE nombre_usuario = ? AND contrasena = ?"
                )
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
        """
        Genera la tabla cruzada de morbilidad diaria por médico para un mes y año específico.

        Retorna un diccionario con la siguiente estructura:
        {
            grupo_profesional: {
                especialidad: {
                    medico: { 1..31: int, 'total': int }
                }
            }
        }
        Ecografía se incluye bajo su grupo ('Doctor') como cualquier otra especialidad,
        y el módulo de exportación se encarga de renderizarla por separado al final.
        """
        conexion = self.conexion_db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                consulta = """
                    SELECT e.grupo_profesional, e.nombre AS especialidad, m.nombre_medico,
                           CAST(strftime('%d', md.fecha) AS INTEGER) AS dia,
                           SUM(md.cantidad_pacientes) as total_dia
                    FROM medicos m
                    JOIN especialidades e ON m.id_especialidad = e.id_especialidad
                    LEFT JOIN morbilidad_diaria md ON m.id_medico = md.id_medico
                        AND CAST(strftime('%m', md.fecha) AS INTEGER) = ?
                        AND CAST(strftime('%Y', md.fecha) AS INTEGER) = ?
                    GROUP BY e.grupo_profesional, e.nombre, m.nombre_medico, dia
                    ORDER BY e.grupo_profesional ASC, e.nombre ASC, m.nombre_medico ASC
                """
                cursor.execute(consulta, (int(mes), int(anio)))
                resultados = cursor.fetchall()

                datos_procesados = {}
                for grupo, especialidad, medico, dia, total_dia in resultados:
                    if grupo not in datos_procesados:
                        datos_procesados[grupo] = {}
                    if especialidad not in datos_procesados[grupo]:
                        datos_procesados[grupo][especialidad] = {}
                    if medico not in datos_procesados[grupo][especialidad]:
                        datos_procesados[grupo][especialidad][medico] = {
                            d: 0 for d in range(1, 32)
                        }
                        datos_procesados[grupo][especialidad][medico]["total"] = 0

                    if dia is not None:
                        datos_procesados[grupo][especialidad][medico][dia] = int(
                            total_dia
                        )
                        datos_procesados[grupo][especialidad][medico]["total"] += int(
                            total_dia
                        )

                return datos_procesados
            except Exception as e:
                print(f"Error al generar relación mensual: {e}")
                return {}
            finally:
                self.conexion_db.desconectar(conexion)
        return {}
