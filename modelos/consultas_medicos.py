"""
Módulo...
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

                # Convertimos el resultado de MySQL a una lista simple de texto
                lista_especialidades = [fila[0] for fila in resultados]
                return lista_especialidades

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
                # Sentencia SQL con JOIN adaptada exactamente a tus tablas y columnas
                consulta = """
                    SELECT m.nombre_medico 
                    FROM medicos m
                    JOIN especialidades e ON m.id_especialidad = e.id_especialidad
                    WHERE e.nombre = %s
                    ORDER BY m.nombre_medico ASC
                """
                cursor.execute(consulta, (nombre_especialidad,))
                resultados = cursor.fetchall()

                # Devolvemos exactamente lo que está guardado en 'nombre_medico'
                lista_medicos = [fila[0] for fila in resultados]
                return lista_medicos

            except Exception as e:
                print(f"Error al consultar médicos: {e}")
                return []
            finally:
                self.conexion_db.desconectar(conexion)
        return []
