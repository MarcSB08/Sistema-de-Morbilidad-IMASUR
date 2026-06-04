<p align="center">
  <img src="assets/logo_imasur.png" alt="Logo IMASUR" width="200"/>
</p>

<h1 align="center">Sistema de Morbilidad IMASUR</h1>

<p align="center">
  <strong>Sistema de Información para el Registro Estadístico de Pacientes</strong><br>
  <em>Proyecto de Servicio Comunitario - Universidad Santa María (USM)</em>
</p>

---

## Descripción General

El **Sistema de Morbilidad IMASUR** es una herramienta de escritorio desarrollada a la medida para el Instituto Municipal Autónomo de Atención y Cooperación para la Salud de Urbaneja (Lechería, Estado Anzoátegui). 

Su objetivo principal es modernizar y optimizar el trabajo del personal de Registros Médicos mediante la captura, procesamiento y visualización de datos numéricos sobre la afluencia de pacientes por especialista. Todo esto operando bajo un entorno local aislado y seguro, garantizando la privacidad absoluta al no registrar información de identidad personal de los pacientes.

## Características Principales

* **Gestión de Morbilidad:** Registro rápido y validado de la cantidad de pacientes atendidos por fecha y médico especialista.
* **Prevención de Duplicados:** Detección inteligente de registros existentes para un mismo médico en la misma fecha, permitiendo la actualización segura de los datos.
* **Reportes Estadísticos Visuales:** Generación de gráficos de torta (Mensuales y Trimestrales) para comparar la afluencia entre médicos de una misma especialidad, o entre distintos grupos profesionales. Opción de exportación a `.png` con fondo sólido.
* **Visor de Relación Mensual (Formato ACT):** Visualización interactiva en formato de hoja de cálculo oscura, con una herramienta secundaria para renderizar la tabla institucional oficial con totales calculados dinámicamente.
* **Base de Datos Auto-gestionada:** Sistema embebido sin necesidad de servidores externos.

## Tecnologías Utilizadas

* **Lenguaje:** Python 3.8.10
* **Interfaz Gráfica:** CustomTkinter (`ctk`), Tkinter (`ttk`)
* **Gráficos:** Matplotlib (`FigureCanvasTkAgg`)
* **Base de Datos:** SQLite (`sqlite3`)
* **Componentes Adicionales:** `tkcalendar`, `babel`

## Instalación y Entorno de Desarrollo

Para ejecutar el código fuente de forma local, tener instalado **Python 3.8.10**.

1. **Clonar el repositorio:**
```bash
git clone [https://github.com/tu-usuario/sistema-de-morbilidad-imasur.git](https://github.com/tu-usuario/sistema-de-morbilidad-imasur.git)
cd sistema-de-morbilidad-imasur
```

2. **Crear y activar el entorno virtual:**
```bash
py -3.8 -m venv venv
venv\Scripts\activate
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

4. Ejecutar la aplicación
```bash
python main.py
```

## Compilación

Ejecuta el siguiente comando en la raíz del proyecto (con el entorno virtual activado):
```bash
pyinstaller --noconsole --onedir --add-data "assets;assets" --icon="assets/logo_imasur.png" --add-data "scripts_sql;scripts_sql" --hidden-import babel.numbers --hidden-import babel.dates --collect-data tkcalendar main.py
```