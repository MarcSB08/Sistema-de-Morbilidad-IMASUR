"""
Módulo que permite comprobar la conexión con la base de datos,
con detección automática de entorno (Desarrollo vs Producción).
"""

import mysql.connector
from mysql.connector import Error
import sys


class ConexionDB:
    def __init__(self):
        # Detecta si el programa se está ejecutando como un .exe compilado
        if getattr(sys, "frozen", False):
            # ==========================================
            # ENTORNO DE PRODUCCIÓN (Clínica IMASUR)
            # Se activa solo cuando abren el .exe
            # ==========================================
            self.host = "192.168.1.50"  # IMPORTANTE: Cambia esto por la IP real del servidor de la clínica
            self.database = "imasur_estadisticas"
            self.user = "root"
            self.password = (
                "MASB_11_2005*"  # Asegúrate de que coincida con la del servidor
            )

        else:
            # ==========================================
            # ENTORNO DE DESARROLLO (Tu Computadora)
            # Se activa cuando ejecutas 'python main.py'
            # ==========================================
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
