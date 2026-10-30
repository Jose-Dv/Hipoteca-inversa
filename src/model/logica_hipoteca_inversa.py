"""Cálculo de desembolso mensual de una hipoteca inversa."""

from dataclasses import dataclass

TASA_MAXIMA_USURA: float = 0.04
PLAZO_MAXIMO_MESES: int = 240
PLAZO_MINIMO_MESES: int = 1


@dataclass(frozen=True)
class ParametrosHipoteca:
    """Agrupa los datos de entrada del cálculo de hipoteca inversa."""

    valor_inmueble: float
    porcentaje: float
    tasa_mensual: float
    plazo_meses: int


class HipotecaInversaError(Exception):
    """Clase base para las excepciones del cálculo de hipoteca inversa."""


class ValorPropiedadCero(HipotecaInversaError):
    def __init__(self, valor_inmueble: float) -> None:
        self.valor_inmueble = valor_inmueble
        super().__init__(
            f"Error: el valor del inmueble debe ser mayor que cero "
            f"(recibido: {valor_inmueble})."
        )


class HipotecaUsura(HipotecaInversaError):
    def __init__(self, tasa_mensual: float, tasa_maxima: float) -> None:
        self.tasa_mensual = tasa_mensual
        self.tasa_maxima = tasa_maxima
        super().__init__(
            f"Error: la tasa mensual ({tasa_mensual*100:.2f}%) supera el máximo "
            f"permitido ({tasa_maxima*100:.0f}%)."
        )


class PlazoMayorPermitido(HipotecaInversaError):
    def __init__(self, plazo_meses: int, plazo_maximo: int) -> None:
        self.plazo_meses = plazo_meses
        self.plazo_maximo = plazo_maximo
        super().__init__(
            f"Error: el plazo ({plazo_meses} meses) no debe ser mayor a {plazo_maximo} meses."
        )


class PlazoMenorIgualCero(HipotecaInversaError):
    def __init__(self, plazo_meses: int, plazo_minimo: int, plazo_maximo: int) -> None:
        self.plazo_meses = plazo_meses
        self.plazo_minimo = plazo_minimo
        self.plazo_maximo = plazo_maximo
        super().__init__(
            f"Error: el plazo ({plazo_meses} meses) debe estar entre "
            f"{plazo_minimo} y {plazo_maximo} meses."
        )


def validar_valor_inmueble(valor_inmueble: float) -> None:
    if valor_inmueble <= 0:
        raise ValorPropiedadCero(valor_inmueble)


def validar_tasa_mensual(tasa_mensual: float) -> None:
    if tasa_mensual > TASA_MAXIMA_USURA:
        raise HipotecaUsura(tasa_mensual, TASA_MAXIMA_USURA)


def validar_plazo_meses(plazo_meses: int) -> None:
    if plazo_meses > PLAZO_MAXIMO_MESES:
        raise PlazoMayorPermitido(plazo_meses, PLAZO_MAXIMO_MESES)
    if plazo_meses < PLAZO_MINIMO_MESES:
        raise PlazoMenorIgualCero(plazo_meses, PLAZO_MINIMO_MESES, PLAZO_MAXIMO_MESES)


def validar_parametros(parametros: ParametrosHipoteca) -> None:
    """Ejecuta cada validador de negocio sobre los parámetros de entrada."""
    validar_valor_inmueble(parametros.valor_inmueble)
    validar_tasa_mensual(parametros.tasa_mensual)
    validar_plazo_meses(parametros.plazo_meses)


def calcular_monto_prestamo(parametros: ParametrosHipoteca) -> float:
    return parametros.valor_inmueble * parametros.porcentaje


def calcular_cuota_mensual(parametros: ParametrosHipoteca) -> float:
    monto_prestamo = calcular_monto_prestamo(parametros)
    if parametros.tasa_mensual == 0:
        return monto_prestamo / parametros.plazo_meses
    tasa = parametros.tasa_mensual
    return (monto_prestamo * tasa) / (1 - (1 + tasa) ** -parametros.plazo_meses)


def calcular_total_abonos(parametros: ParametrosHipoteca) -> float:
    return calcular_cuota_mensual(parametros) * parametros.plazo_meses


def calcular_total_intereses(parametros: ParametrosHipoteca) -> float:
    return calcular_total_abonos(parametros) - calcular_monto_prestamo(parametros)


def desembolso_mensual(parametros: ParametrosHipoteca) -> tuple[float, float, float]:
    """
    Calcula la cuota mensual, el total de abonos y el total de intereses.

    Raises:
        ValorPropiedadCero, HipotecaUsura, PlazoMayorPermitido, PlazoMenorIgualCero
    """
    validar_parametros(parametros)

    cuota_mensual = calcular_cuota_mensual(parametros)
    total_abonos = calcular_total_abonos(parametros)
    total_intereses = calcular_total_intereses(parametros)

    return cuota_mensual, total_abonos, total_intereses
