"""
Módulo que maneja las consultas a la base de datos relacionadas con los médicos y la morbilidad.
"""

from modelos.conexion_db import ConexionDB


class ConsultasMedicos:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def obtener_especialidades(self):
        conexion = self.conexion_db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT nombre FROM especialidades ORDER BY nombre ASC")
                resultados = cursor.fetchall()

                lista_especialidades = [fila[0] for fila in resultados]
                return lista_especialidades

            except Exception as e:
                print(f"Error al consultar especialidades: {e}")
                return []
            finally:
                self.conexion_db.desconectar(conexion)
        return []

    def obtener_medicos_por_especialidad(self, nombre_especialidad):
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

                lista_medicos = [fila[0] for fila in resultados]
                return lista_medicos

            except Exception as e:
                print(f"Error al consultar médicos: {e}")
                return []
            finally:
                self.conexion_db.desconectar(conexion)
        return []

    def guardar_registro_morbilidad(self, fecha, nombre_medico, cantidad_pacientes):
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
