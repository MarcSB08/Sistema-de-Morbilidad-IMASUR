"""
Este módulo permite realizar la conexión con la base de datos donde se lleva el registro
de los pacientes atendidos por especialista.
"""

import mysql.connector
from mysql.connector import Error


class ConexionIMASUR:
    def __init__(self):
        self.host = "127.0.0.1"
        self.database = "imasur_estadisticas"
        self.user = "root"
        self.password = "MASB_11_2005*"

    def conectar(self):
        try:
            conexion = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
            )
            if conexion.is_connected():
                print("¡Conexión exitosa a la base de datos del IMASUR!")
                return conexion

        except Error as e:
            print(f"Error al conectar con MySQL: {e}")
            return None


if __name__ == "__main__":
    db = ConexionIMASUR()
    db.conectar()
