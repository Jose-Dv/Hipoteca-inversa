"""Interfaz de consola de la aplicación de hipoteca inversa.

Pide los datos del cálculo, se los entrega a `hipoteca_controller` y muestra
el resultado o el mensaje de error. Los mismos controladores los usa la
interfaz gráfica en Kivy (`interfaz_kivy.py`). Esta vista no contiene lógica
de negocio ni de validación de formato.

Ejecución, desde la raíz del proyecto: python src/view/console.py
"""

import sys
sys.path.append("src")

from controller import hipoteca_controller as controlador


def pedir_texto(mensaje: str) -> str:
    """Pide un dato al usuario sin dejar que el programa truene si la
    entrada se interrumpe (Ctrl+C) o se acaba de forma abrupta (EOF)."""
    try:
        return input(mensaje)
    except (EOFError, KeyboardInterrupt):
        print("\nOperación cancelada por el usuario.")
        sys.exit(0)


def pedir_datos() -> tuple[str, str, str, str]:
    valor = pedir_texto("Valor Propiedad: ")
    porcentaje = pedir_texto("Porcentaje de desembolso: ")
    tasa = pedir_texto("Tasa de interes: ")
    plazo = pedir_texto("Plazo en meses: ")
    return valor, porcentaje, tasa, plazo


def mostrar_resultado(resultado: controlador.ResultadoHipoteca) -> None:
    print("Cuota mensual:", f"{resultado.cuota_mensual:,.2f}")
    print("Total abonos:", f"{resultado.total_abonos:,.2f}")
    print("Total intereses:", f"{resultado.total_intereses:,.2f}")


def calcular_hipotecas() -> None:
    print(
        "Este programa permite calcular la hipoteca inversa, en base a: \n"
        " 1.Valor Propiedad \n"
        " 2.Porcentaje de desembolso \n"
        " 3.Tasa de interes \n"
        " 4.Plazo en meses "
    )

    while True:
        valor, porcentaje, tasa, plazo = pedir_datos()

        try:
            resultado = controlador.calcular_hipoteca(valor, porcentaje, tasa, plazo)
        except controlador.ErrorCalculoHipoteca as error:
            # Cubre tanto datos con formato inválido (texto no numérico)
            # como el incumplimiento de una regla de negocio del modelo.
            print(f"\n{error}\n")
        else:
            mostrar_resultado(resultado)

        continuar = pedir_texto("\n¿Desea calcular otra hipoteca? (s/n): ")
        if continuar.strip().lower() not in ("s", "si", "sí"):
            break


if __name__ == "__main__":
    calcular_hipotecas()
