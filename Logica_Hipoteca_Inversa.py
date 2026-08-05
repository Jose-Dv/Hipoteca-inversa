# Aqui se encuentra la logica de el proyecto "Calculadora de Hipoteca Inversa"

def calcular_cuota_mensual(valor_inmueble: float, porcentaje: float, tasa_mensual: float, plazo_meses: int) -> float:
    """ Calcula la cuota mensual que el banco le pagaría a una persona que toma una hipoteca inversa,
    usando como base un porcentaje del valor del inmueble y la fórmula de anualidad. """
    
    V = valor_inmueble * porcentaje
    i = tasa_mensual
    n = plazo_meses

    if i == 0:
        cuota_mensual = V / n
    else:
        cuota_mensual = V * i / (1 - (1 + i) ** -n)

    return f"La cuota mensual por parte del banco al usuario es de: {cuota_mensual}"
