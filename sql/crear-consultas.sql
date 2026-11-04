-- Crea la tabla consultas (es la misma que crea la aplicación por sí sola).
CREATE TABLE IF NOT EXISTS consultas (
    id VARCHAR(36) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL DEFAULT '',
    valor_inmueble DOUBLE PRECISION NOT NULL,
    porcentaje DOUBLE PRECISION NOT NULL,
    tasa_mensual DOUBLE PRECISION NOT NULL,
    plazo_meses INTEGER NOT NULL,
    cuota_mensual DOUBLE PRECISION NOT NULL,
    total_abonos DOUBLE PRECISION NOT NULL,
    total_intereses DOUBLE PRECISION NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT NOW()
);
