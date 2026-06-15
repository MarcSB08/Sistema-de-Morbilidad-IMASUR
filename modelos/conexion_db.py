"""
Módulo que permite comprobar la conexión con la base de datos SQLite.
"""

import os
import sqlite3
import sys
from sqlite3 import Error


class ConexionDB:
    def __init__(self):
        if getattr(sys, "frozen", False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        db_dir = os.path.join(base_dir, "database")
        os.makedirs(db_dir, exist_ok=True)

        self.database = os.path.join(db_dir, "imasur_estadisticas.db")

    def conectar(self):
        try:
            conexion = sqlite3.connect(self.database)
            return conexion
        except Error as e:
            print(f"Error al conectar a SQLite: {e}")
            return None

    def desconectar(self, conexion):
        if conexion:
            conexion.close()
