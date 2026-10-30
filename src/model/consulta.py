"""Registro de una consulta de hipoteca inversa."""

import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Consulta:
    """Datos ingresados y resultados de una consulta. ``nombre`` puede ir vacío.

    ``id`` es un UUID en texto, generado al crear la consulta; no cuenta al
    comparar dos consultas.
    """

    nombre: str
    valor_inmueble: float
    porcentaje: float
    tasa_mensual: float
    plazo_meses: int
    cuota_mensual: float
    total_abonos: float
    total_intereses: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()), compare=False)
