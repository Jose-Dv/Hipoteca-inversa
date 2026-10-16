CREATE TABLE IF NOT EXISTS solicitudes (
    id_solicitud SERIAL PRIMARY KEY,
    id_cliente INT,
    fecha_solicitud DATE,
    estado VARCHAR(30)
);
