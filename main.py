"""
Módulo principal del sistema, donde se inicializa la interfaz visual.
"""

from vistas.ventana_principal import VentanaPrincipal

if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
