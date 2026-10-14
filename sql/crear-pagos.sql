CREATE TABLE pagos (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    id_hipoteca INT,
    valor_pago DECIMAL(15,2),
    fecha_pago DATE
);
