-- Agrega 3 consultas de ejemplo (los valores salen de las pruebas unitarias).
-- Ejecute antes crear-consultas.sql.
INSERT INTO consultas (id, nombre, valor_inmueble, porcentaje, tasa_mensual, plazo_meses,
                       cuota_mensual, total_abonos, total_intereses)
VALUES
    (gen_random_uuid()::text, 'Ana Prueba Uno', 300000000, 0.40, 0.012, 120,
     1892165.77, 227059892.25, 107059892.25),
    (gen_random_uuid()::text, 'Carlos Zapata', 500000000, 0.30, 0.015, 48,
     4406249.94, 211499997.18, 61499997.18),
    (gen_random_uuid()::text, 'Demo Tres', 150000000, 0.50, 0.009, 60,
     1623211.07, 97392664.32, 22392664.32);
