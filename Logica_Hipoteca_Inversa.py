# Aqui se encuentra la logica de el proyecto "Calculadora de Hipoteca Inversa" y la clase de exepciones 

class HipotecaInversaError(Exception):
    pass
    
def desembolso_mensual(valor_inmueble: float, porcentaje: float, tasa_mensual: float, plazo_meses: int):
    """ Calcula la cuota mensual que el banco le pagaría a una persona que toma una hipoteca inversa,
    usando como base un porcentaje del valor del inmueble y la fórmula de anualidad. """
    
    if valor_inmueble <= 0:
        raise HipotecaInversaError("Valor del inmueble invalido: debe ser mayor que cero")

    if tasa_mensual > 0.04:
        raise HipotecaInversaError("Tasa mensual invalida: supera el maximo de usura permitido (4%)")

    if plazo_meses < 1 or plazo_meses > 240:
        raise HipotecaInversaError("Plazo invalido: el numero de meses debe estar entre 1 y 240")

    V = valor_inmueble * porcentaje
    i = tasa_mensual
    n = plazo_meses

    if i == 0:
        cuota = V / n
    else:
        cuota = V * i / (1 - (1 + i) ** -n)

    abonos = cuota * n
    intereses = abonos - V

    return cuota, abonos, intereses
