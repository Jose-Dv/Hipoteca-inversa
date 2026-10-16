"""Interfaz de consola de la aplicación de hipoteca inversa.

Ofrece un menú con tres opciones:

1. Calcular una hipoteca inversa (delegado a `hipoteca_controller`).
2. Registrar un cliente en la base de datos (delegado a `cliente_controller`).
3. Buscar clientes por cédula o por nombre/apellido (`cliente_controller`).

Los mismos controladores los usa la interfaz gráfica en Kivy
(`interfaz_kivy.py`). Esta vista no contiene lógica de negocio ni de
validación de formato: solo captura texto, se lo pasa al controlador y
muestra el resultado o el mensaje de error.
"""

import sys
from pathlib import Path

# Permite ejecutar este archivo de cualquier forma: `python src/view/console.py`,
# `python -m src.view.console`, o desde el botón "Run" de un editor (que
# normalmente ejecuta el archivo de forma directa). En todos los casos se
# agrega la raíz del proyecto a sys.path para que `import src...` funcione.
_RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
if str(_RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(_RAIZ_PROYECTO))

from src.controller import cliente_controller as clientes  # noqa: E402
from src.controller import hipoteca_controller as controlador  # noqa: E402


def pedir_texto(mensaje: str) -> str:
    """Pide un dato al usuario sin dejar que el programa truene si la
    entrada se interrumpe (Ctrl+C) o se acaba de forma abrupta (EOF)."""
    try:
        return input(mensaje)
    except (EOFError, KeyboardInterrupt):
        print("\nOperación cancelada por el usuario.")
        sys.exit(0)


# ---------------------------------------------------------------------------
# Opción 1: calcular hipoteca
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Opción 2: registrar cliente
# ---------------------------------------------------------------------------

def registrar_cliente() -> None:
    print("\n--- Registrar cliente ---")
    cedula = pedir_texto("Cédula: ")
    nombres = pedir_texto("Nombres: ")
    apellidos = pedir_texto("Apellidos: ")
    nacimiento = pedir_texto("Fecha de nacimiento (AAAA-MM-DD, opcional): ")
    telefono = pedir_texto("Teléfono (opcional): ")
    direccion = pedir_texto("Dirección (opcional): ")

    try:
        cliente = clientes.insertar_cliente(
            cedula, nombres, apellidos, nacimiento, telefono, direccion
        )
    except clientes.ErrorCliente as error:
        print(f"\n{error}")
    else:
        print(f"\nCliente guardado con id {cliente.id_cliente}.")


# ---------------------------------------------------------------------------
# Opción 3: buscar cliente
# ---------------------------------------------------------------------------

def buscar_cliente() -> None:
    print("\n--- Buscar cliente ---")
    consulta = pedir_texto("Escriba la cédula, o parte del nombre o apellido: ").strip()

    try:
        if consulta.isdigit():
            cliente = clientes.buscar_cliente_por_cedula(consulta)
            encontrados = [] if cliente is None else [cliente]
        else:
            encontrados = clientes.buscar_clientes(consulta)
    except clientes.ErrorCliente as error:
        print(f"\n{error}")
        return

    if not encontrados:
        print("\nNo se encontraron clientes.")
        return

    print(f"\nSe encontraron {len(encontrados)} cliente(s):")
    for cliente in encontrados:
        print("\n" + clientes.formatear_cliente(cliente))


# ---------------------------------------------------------------------------
# Menú principal
# ---------------------------------------------------------------------------

def mostrar_menu() -> None:
    print(
        "\n=== Hipoteca Inversa ===\n"
        " 1. Calcular hipoteca\n"
        " 2. Registrar cliente\n"
        " 3. Buscar cliente\n"
        " 4. Salir"
    )


def main() -> None:
    acciones = {
        "1": calcular_hipotecas,
        "2": registrar_cliente,
        "3": buscar_cliente,
    }

    while True:
        mostrar_menu()
        opcion = pedir_texto("Seleccione una opción: ").strip()

        if opcion == "4":
            print("¡Hasta luego!")
            break

        accion = acciones.get(opcion)
        if accion is None:
            print("Opción no válida. Escriba 1, 2, 3 o 4.")
        else:
            accion()


if __name__ == "__main__":
    main()
