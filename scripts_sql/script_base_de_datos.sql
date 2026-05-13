CREATE DATABASE imasur_estadisticas;
USE imasur_estadisticas;

CREATE TABLE especialidades (
    id_especialidad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    grupo_profesional VARCHAR(50) NOT NULL
);

CREATE TABLE medicos (
    id_medico INT AUTO_INCREMENT PRIMARY KEY,
    nombre_medico VARCHAR(150) NOT NULL,
    id_especialidad INT NOT NULL,
    FOREIGN KEY (id_especialidad) REFERENCES especialidades(id_especialidad)
);

CREATE TABLE morbilidad_diaria (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    id_medico INT NOT NULL,
    cantidad_pacientes INT NOT NULL,
    FOREIGN KEY (id_medico) REFERENCES medicos(id_medico)
);

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL,
    contrasena VARCHAR(50) NOT NULL
);

INSERT INTO usuarios (nombre_usuario, contrasena) VALUES ('admin', '123456');