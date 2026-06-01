"""
Módulo que permite comprobar la conexión con la base de datos.
"""

import mysql.connector
from mysql.connector import Error
import sys


class ConexionDB:
    def __init__(self):
        if getattr(sys, "frozen", False):
            self.host = "10.0.0.46"  # 10.0.0.46
            self.database = "imasur_estadisticas"
            self.user = "INFORMATICA"  # INFORMATICA
            self.password = ""  # ""

        else:
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
                return conexion
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return None

    def desconectar(self, conexion):
        if conexion and conexion.is_connected():
            conexion.close()
