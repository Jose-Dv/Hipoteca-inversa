CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    correo VARCHAR(100),
    password VARCHAR(255),
    rol VARCHAR(20)
);
