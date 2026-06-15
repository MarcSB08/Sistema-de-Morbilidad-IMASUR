"""
Módulo principal del sistema, donde se inicializa la aplicación con el login.
"""

import os
import sys

from inicializar_sqlite import inicializar_db
from vistas.login import Login

if __name__ == "__main__":
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    db_path = os.path.join(base_dir, "database", "imasur_estadisticas.db")

    if not os.path.exists(db_path):
        print("Base de datos no detectada. Generando archivo inicial...")
        inicializar_db()

    app = Login()
    app.mainloop()
