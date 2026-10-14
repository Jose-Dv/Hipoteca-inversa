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
(1, CURDATE(), 'PENDIENTE'),
(2, CURDATE(), 'APROBADA');

-- VALUACIONES
INSERT INTO valuaciones (
    id_vivienda,
    valor_estimado,
    fecha_valuacion
)
VALUES
(1, 460000000, CURDATE()),
(2, 390000000, CURDATE());

-- HIPOTECAS
INSERT INTO hipotecas (
    id_cliente,
    id_vivienda,
    monto_aprobado,
    tasa_interes,
    fecha_inicio
)
VALUES
(1, 1, 230000000, 7.50, CURDATE()),
(2, 2, 190000000, 7.20, CURDATE());

-- PAGOS
INSERT INTO pagos (
    id_hipoteca,
    valor_pago,
    fecha_pago
)
VALUES
(1, 1500000, CURDATE()),
(2, 1200000, CURDATE());

-- BENEFICIARIOS
INSERT INTO beneficiarios (
    id_cliente,
    nombre,
    parentesco
)
VALUES
(1, 'Carlos Pérez', 'Hijo'),
(2, 'Ana Gómez', 'Hija');
