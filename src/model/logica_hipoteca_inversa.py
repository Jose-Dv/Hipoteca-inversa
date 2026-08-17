#Exepciones de el aplicativo

class ValorPropiedad0(Exception):
    """exepcion que se dispara cuando el valor de la propiedad es 0"""
    pass


class HipotecaUsura(Exception):
    """exepcion que se dispara cuando el porcentaje de la tasa supera el 4%"""
    pass


class PlazoMayor240(Exception):
    """exepcion que se dispara cuando el plazo de meses es mayor a 240"""
    pass


class PlazoMenorIgual0(Exception):
    """exepcion que se dispara cuando el plazo de meses es menor igual a 0"""
    pass


# Aqui se encuentra la logica de el proyecto "Calculadora de Hipoteca Inversa"

def desembolso_mensual(valor_inmueble: float, porcentaje: float, tasa_mensual: float, plazo_meses: int):
    """ Calcula la cuota mensual que el banco le pagaría a una persona que toma una hipoteca inversa,
    usando como base un porcentaje del valor del inmueble y la fórmula de anualidad. """
    
    if valor_inmueble <= 0:
        raise ValorPropiedad0("Valor del inmueble invalido: debe ser mayor que cero")

    if tasa_mensual > 0.04:
        raise HipotecaUsura("Tasa mensual invalida: supera el maximo de usura permitido (4%)")

    if plazo_meses > 240:
        raise PlazoMayor240("Plazo invalido: el numero de meses no debe ser mayor a 240")

    if plazo_meses <= 0:
        raise PlazoMenorIgual0("Plazo invalido: el numero de meses debe estar entre 1 y 240")


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
