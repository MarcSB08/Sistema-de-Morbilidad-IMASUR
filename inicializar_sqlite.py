import os
import sqlite3


def inicializar_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    db_dir = os.path.join(base_dir, "database")
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "imasur_estadisticas.db")

    print(f"Configurando base de datos en: {db_path}")
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()

    tablas_sql = """
    CREATE TABLE IF NOT EXISTS especialidades (
        id_especialidad INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(100) NOT NULL,
        grupo_profesional VARCHAR(50) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS medicos (
        id_medico INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_medico VARCHAR(150) NOT NULL,
        id_especialidad INTEGER NOT NULL,
        FOREIGN KEY (id_especialidad) REFERENCES especialidades(id_especialidad)
    );

    CREATE TABLE IF NOT EXISTS morbilidad_diaria (
        id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha DATE NOT NULL,
        id_medico INTEGER NOT NULL,
        cantidad_pacientes INTEGER NOT NULL,
        FOREIGN KEY (id_medico) REFERENCES medicos(id_medico)
    );

    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_usuario VARCHAR(50) NOT NULL,
        contrasena VARCHAR(50) NOT NULL
    );
    """
    cursor.executescript(tablas_sql)

    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE nombre_usuario = 'admin'")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO usuarios (nombre_usuario, contrasena) VALUES ('admin', '123456')"
        )
        print("- Usuario 'admin' creado exitosamente.")

    cursor.execute("SELECT COUNT(*) FROM especialidades")
    if cursor.fetchone()[0] == 0:
        ruta_sql = os.path.join(base_dir, "scripts_sql", "directorio_medico.sql")
        if os.path.exists(ruta_sql):
            with open(ruta_sql, "r", encoding="utf-8") as archivo_sql:
                script_medicos = archivo_sql.read()
                script_medicos = script_medicos.replace("USE imasur_estadisticas;", "")
                cursor.executescript(script_medicos)
            print("- Directorio médico cargado exitosamente.")
        else:
            print(f"- Advertencia: No se encontró el archivo {ruta_sql}.")

    conexion.commit()
    conexion.close()
    print(
        "¡Base de datos SQLite inicializada y lista para usarse dentro de la carpeta 'database'!"
    )


if __name__ == "__main__":
    inicializar_db()
