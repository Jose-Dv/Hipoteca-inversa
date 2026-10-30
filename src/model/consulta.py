"""Registro de una consulta de hipoteca inversa."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Consulta:
    """Datos ingresados y resultados de una consulta. ``nombre`` puede ir vacío.

    ``id`` lo asigna la base de datos; no cuenta al comparar dos consultas.
    """

    nombre: str
    valor_inmueble: float
    porcentaje: float
    tasa_mensual: float
    plazo_meses: int
    cuota_mensual: float
    total_abonos: float
    total_intereses: float
    id: int | None = field(default=None, compare=False)
