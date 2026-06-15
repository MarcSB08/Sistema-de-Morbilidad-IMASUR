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

INSERT INTO usuarios (nombre_usuario, contrasena) VALUES ('fanny', '123456');
