CREATE TABLE IF NOT EXISTS viviendas (
    id_vivienda SERIAL PRIMARY KEY,
    id_cliente INT,
    direccion VARCHAR(200),
    valor_comercial DECIMAL(15,2),
    tipo_vivienda VARCHAR(50)
);
