CREATE TABLE IF NOT EXISTS hipotecas (
    id_hipoteca SERIAL PRIMARY KEY,
    id_cliente INT,
    id_vivienda INT,
    monto_aprobado DECIMAL(15,2),
    tasa_interes DECIMAL(5,2),
    fecha_inicio DATE
);
