"""Controlador de clientes: validación y acceso a PostgreSQL.

Las vistas (consola y Kivy) solo llaman a estas funciones y capturan
``ErrorCliente``. Los datos de conexión (PGHOST, PGDATABASE, PGUSER,
PGPASSWORD y PGPORT) se leen de ``secret_config.py``.
"""

from contextlib import contextmanager
from datetime import date, datetime
from pathlib import Path
from typing import Iterator, Optional

import psycopg2
from psycopg2 import errors

from src.model.cliente import Cliente

CARPETA_SQL = Path(__file__).resolve().parents[2] / "sql"
ARCHIVOS_CREAR_TABLAS = (
    "crear-clientes.sql",
    "crear-usuarios.sql",
    "crear-viviendas.sql",
    "crear-hipotecas.sql",
    "crear-solicitudes.sql",
)
TABLAS = ("solicitudes", "hipotecas", "viviendas", "usuarios", "clientes")

LONGITUD_MAXIMA_CEDULA = 20
LONGITUD_MAXIMA_NOMBRE = 100
LONGITUD_MAXIMA_TELEFONO = 20
LONGITUD_MAXIMA_DIRECCION = 200
FORMATO_FECHA = "%Y-%m-%d"
COLUMNAS_CLIENTE = (
    "id_cliente, cedula, nombres, apellidos, fecha_nacimiento, telefono, direccion"
)


class ErrorCliente(Exception):
    """Error de validación o de base de datos al gestionar clientes."""


@contextmanager
def _conexion() -> Iterator:
    """Abre una conexión, confirma al terminar y siempre la cierra.

    ``secret_config`` se importa aquí, y no al inicio, para que calcular una
    hipoteca funcione aunque todavía no exista ese archivo.
    """
    try:
        import secret_config  # pylint: disable=import-outside-toplevel
    except ImportError as error:
        raise ErrorCliente(
            "No se encontró secret_config.py. Copie secret_config_sample.py como "
            "secret_config.py y complete los datos de su base de datos."
        ) from error

    try:
        conexion = psycopg2.connect(
            host=secret_config.PGHOST,
            dbname=secret_config.PGDATABASE,
            user=secret_config.PGUSER,
            password=secret_config.PGPASSWORD,
            port=secret_config.PGPORT,
        )
    except psycopg2.Error as error:
        raise ErrorCliente(
            "No fue posible conectar con la base de datos. "
            "Revise los datos de secret_config.py."
        ) from error
    try:
        with conexion:
            yield conexion
    finally:
        conexion.close()


def crear_tablas() -> None:
    """Crea las tablas del proyecto si todavía no existen."""
    with _conexion() as conexion, conexion.cursor() as cursor:
        for archivo in ARCHIVOS_CREAR_TABLAS:
            cursor.execute((CARPETA_SQL / archivo).read_text(encoding="utf-8"))


def borrar_tablas() -> None:
    """Elimina las tablas del proyecto. Borra todos sus datos."""
    with _conexion() as conexion, conexion.cursor() as cursor:
        for tabla in TABLAS:
            cursor.execute(f"DROP TABLE IF EXISTS {tabla} CASCADE")


def _validar_cedula(cedula: str) -> str:
    cedula = cedula.strip()
    if not cedula.isdigit():
        raise ErrorCliente("La cédula es obligatoria y debe contener solo números.")
    if len(cedula) > LONGITUD_MAXIMA_CEDULA:
        raise ErrorCliente(
            f"La cédula no puede tener más de {LONGITUD_MAXIMA_CEDULA} dígitos."
        )
    return cedula


def _validar_texto_obligatorio(texto: str, nombre_campo: str, maximo: int) -> str:
    texto = texto.strip()
    if not texto:
        raise ErrorCliente(f"Falta completar: {nombre_campo}.")
    if len(texto) > maximo:
        raise ErrorCliente(f"El campo {nombre_campo} no puede superar {maximo} caracteres.")
    return texto


def _validar_texto_opcional(texto: str, nombre_campo: str, maximo: int) -> Optional[str]:
    texto = texto.strip()
    if len(texto) > maximo:
        raise ErrorCliente(f"El campo {nombre_campo} no puede superar {maximo} caracteres.")
    return texto or None


def _validar_fecha_nacimiento(texto: str) -> Optional[date]:
    texto = texto.strip()
    if not texto:
        return None
    try:
        fecha = datetime.strptime(texto, FORMATO_FECHA).date()
    except ValueError as error:
        raise ErrorCliente(
            "La fecha de nacimiento debe tener el formato AAAA-MM-DD (ejemplo: 1990-05-23)."
        ) from error
    if fecha > date.today():
        raise ErrorCliente("La fecha de nacimiento no puede ser futura.")
    return fecha


def insertar_cliente(
    cedula: str,
    nombres: str,
    apellidos: str,
    nacimiento: str = "",
    telefono: str = "",
    direccion: str = "",
) -> Cliente:
    """Valida e inserta un cliente. Retorna el cliente con su ``id_cliente``."""
    cedula = _validar_cedula(cedula)
    nombres = _validar_texto_obligatorio(nombres, "nombres", LONGITUD_MAXIMA_NOMBRE)
    apellidos = _validar_texto_obligatorio(apellidos, "apellidos", LONGITUD_MAXIMA_NOMBRE)
    fecha_nacimiento = _validar_fecha_nacimiento(nacimiento)
    telefono = _validar_texto_opcional(telefono, "teléfono", LONGITUD_MAXIMA_TELEFONO)
    direccion = _validar_texto_opcional(direccion, "dirección", LONGITUD_MAXIMA_DIRECCION)

    consulta = (
        "INSERT INTO clientes (cedula, nombres, apellidos, fecha_nacimiento, telefono, direccion) "
        f"VALUES (%s, %s, %s, %s, %s, %s) RETURNING {COLUMNAS_CLIENTE}"
    )
    parametros = (cedula, nombres, apellidos, fecha_nacimiento, telefono, direccion)
    try:
        with _conexion() as conexion, conexion.cursor() as cursor:
            cursor.execute(consulta, parametros)
            return Cliente(*cursor.fetchone())
    except errors.UniqueViolation as error:
        raise ErrorCliente(f"Ya existe un cliente con la cédula {cedula}.") from error
    except psycopg2.Error as error:
        raise ErrorCliente("No fue posible guardar el cliente en la base de datos.") from error


def buscar_cliente_por_cedula(cedula: str) -> Optional[Cliente]:
    """Retorna el cliente con esa cédula exacta, o ``None`` si no existe."""
    cedula = _validar_cedula(cedula)
    consulta = f"SELECT {COLUMNAS_CLIENTE} FROM clientes WHERE cedula = %s"
    try:
        with _conexion() as conexion, conexion.cursor() as cursor:
            cursor.execute(consulta, (cedula,))
            fila = cursor.fetchone()
    except psycopg2.Error as error:
        raise ErrorCliente("No fue posible consultar la base de datos.") from error
    return None if fila is None else Cliente(*fila)


def buscar_clientes(texto: str) -> list[Cliente]:
    """Busca por parte del nombre o apellido, sin distinguir mayúsculas."""
    texto = texto.strip()
    if not texto:
        raise ErrorCliente("Escriba parte del nombre o apellido para buscar.")
    consulta = (
        f"SELECT {COLUMNAS_CLIENTE} FROM clientes "
        "WHERE nombres ILIKE %s OR apellidos ILIKE %s ORDER BY apellidos, nombres"
    )
    patron = f"%{texto}%"
    try:
        with _conexion() as conexion, conexion.cursor() as cursor:
            cursor.execute(consulta, (patron, patron))
            filas = cursor.fetchall()
    except psycopg2.Error as error:
        raise ErrorCliente("No fue posible consultar la base de datos.") from error
    return [Cliente(*fila) for fila in filas]


def formatear_cliente(cliente: Cliente) -> str:
    """Texto de varias líneas listo para mostrar en cualquier vista."""
    nacimiento = cliente.fecha_nacimiento.isoformat() if cliente.fecha_nacimiento else "-"
    return (
        f"Cédula: {cliente.cedula}\n"
        f"Nombre: {cliente.nombres} {cliente.apellidos}\n"
        f"Nacimiento: {nacimiento}\n"
        f"Teléfono: {cliente.telefono or '-'}\n"
        f"Dirección: {cliente.direccion or '-'}"
    )
