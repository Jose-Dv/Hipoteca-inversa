-- Datos de prueba opcionales (PostgreSQL).
-- Ejecutar DESPUES de crear las tablas (las pruebas unitarias las crean).
-- Las pruebas unitarias borran y recrean las tablas, asi que estos datos
-- se pierden cada vez que se corren.

-- USUARIOS
INSERT INTO usuarios (nombre, correo, password, rol)
VALUES
('Administrador', 'admin@hipoteca.com', '123456', 'ADMIN'),
('Asesor Financiero', 'asesor@hipoteca.com', '123456', 'ASESOR');

-- CLIENTES
INSERT INTO clientes (
    cedula,
    nombres,
    apellidos,
    fecha_nacimiento,
    telefono,
    direccion
)
VALUES
('12345678', 'Juan', 'Pérez', '1955-03-12', '3001234567', 'Medellín'),
('87654321', 'María', 'Gómez', '1958-08-21', '3019876543', 'Bello');

-- VIVIENDAS
INSERT INTO viviendas (
    id_cliente,
    direccion,
    valor_comercial,
    tipo_vivienda
)
VALUES
(1, 'Carrera 50 #45-20 Medellín', 450000000, 'Casa'),
(2, 'Calle 30 #20-15 Bello', 380000000, 'Apartamento');

-- SOLICITUDES
INSERT INTO solicitudes (
    id_cliente,
    fecha_solicitud,
    estado
)
VALUES
(1, CURRENT_DATE, 'PENDIENTE'),
(2, CURRENT_DATE, 'APROBADA');

-- HIPOTECAS
INSERT INTO hipotecas (
    id_cliente,
    id_vivienda,
    monto_aprobado,
    tasa_interes,
    fecha_inicio
)
VALUES
(1, 1, 230000000, 7.50, CURRENT_DATE),
(2, 2, 190000000, 7.20, CURRENT_DATE);
