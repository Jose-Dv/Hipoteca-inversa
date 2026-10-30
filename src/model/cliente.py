"""Entidad Cliente: una fila de la tabla ``clientes``."""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class Cliente:
    """Representa un cliente registrado en la base de datos."""

    id_cliente: Optional[int]
    cedula: str
    nombres: str
    apellidos: str
    fecha_nacimiento: Optional[date] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
