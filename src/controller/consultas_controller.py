"""Guarda, busca y elimina las consultas de hipoteca inversa en PostgreSQL."""

import psycopg2

import secret_config
from model.consulta import Consulta

CREAR_TABLA = """
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
)
"""

INSERTAR = """
INSERT INTO consultas (id, nombre, valor_inmueble, porcentaje, tasa_mensual,
                       plazo_meses, cuota_mensual, total_abonos, total_intereses)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

BUSCAR = """
SELECT nombre, valor_inmueble, porcentaje, tasa_mensual, plazo_meses,
       cuota_mensual, total_abonos, total_intereses, id
FROM consultas
WHERE nombre ILIKE %s
ORDER BY fecha DESC
"""

ELIMINAR = "DELETE FROM consultas WHERE id = %s"


def conectar():
    return psycopg2.connect(
        host=secret_config.PGHOST,
        dbname=secret_config.PGDATABASE,
        user=secret_config.PGUSER,
        password=secret_config.PGPASSWORD,
        port=secret_config.PGPORT,
    )


class ConsultasController:
    """Operaciones con la tabla ``consultas``. La tabla se crea sola si no existe."""

    @staticmethod
    def crear_tabla() -> None:
        conexion = conectar()
        conexion.cursor().execute(CREAR_TABLA)
        conexion.commit()
        conexion.close()

    @staticmethod
    def borrar_tabla() -> None:
        conexion = conectar()
        conexion.cursor().execute("DROP TABLE IF EXISTS consultas")
        conexion.commit()
        conexion.close()

    @staticmethod
    def insertar(consulta: Consulta) -> None:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute(CREAR_TABLA)
        cursor.execute(INSERTAR, (
            consulta.id, consulta.nombre, consulta.valor_inmueble,
            consulta.porcentaje, consulta.tasa_mensual, consulta.plazo_meses,
            consulta.cuota_mensual, consulta.total_abonos, consulta.total_intereses,
        ))
        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar(nombre: str = "") -> list[Consulta]:
        """Busca por parte del nombre, sin distinguir mayúsculas. Sin nombre, trae todas."""
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute(CREAR_TABLA)
        cursor.execute(BUSCAR, (f"%{nombre}%",))
        filas = cursor.fetchall()
        conexion.commit()
        conexion.close()
        return [Consulta(*fila) for fila in filas]

    @staticmethod
    def eliminar(id_consulta: str) -> None:
        """Elimina una sola consulta, identificada por su id (UUID en texto)."""
        conexion = conectar()
        conexion.cursor().execute(ELIMINAR, (id_consulta,))
        conexion.commit()
        conexion.close()
