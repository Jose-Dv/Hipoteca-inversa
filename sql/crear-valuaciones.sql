CREATE TABLE valuaciones (
    id_valuacion INT AUTO_INCREMENT PRIMARY KEY,
    id_vivienda INT,
    valor_estimado DECIMAL(15,2),
    fecha_valuacion DATE
);
