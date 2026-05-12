"""
Módulo principal del sistema, donde se inicializa la aplicación con el login.
"""

from vistas.login import Login

if __name__ == "__main__":
    app = Login()
    app.mainloop()
