# Aqui se encuentra la logica de el proyecto "Calculadora de Hipoteca Inversa"

def desembolso_mensual(valor_inmueble: float, porcentaje: float, tasa_mensual: float, plazo_meses: int) -> tuple[float, float, float]:

    """El proposito de esta funcion, es calcular el desembolso mensual por parte
        de el banco a la persono que esta solicitando dicho servicio recibiendo
        los datos tales como el plazo, """
    
    V = valor_inmueble * porcentaje
    i = tasa_mensual
    n = plazo_meses
    cuota = (V * i) / (1 - (1 + i) ** -n)

    total_abonos = cuota * n
    total_intereses = total_abonos - V

    return cuota, total_abonos, total_intereses

