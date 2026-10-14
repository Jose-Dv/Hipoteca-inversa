CREATE TABLE solicitudes (
    id_solicitud INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    fecha_solicitud DATE,
    estado VARCHAR(30)
);
