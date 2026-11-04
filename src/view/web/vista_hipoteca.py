import sys
sys.path.append("src")

from flask import Blueprint, render_template, request

from model.logica_hipoteca_inversa import (
    ParametrosHipoteca,
    desembolso_mensual,
    HipotecaInversaError,
)
from model.consulta import Consulta
from controller.consultas_controller import ConsultasController

vista = Blueprint("vista", __name__)

PALABRA_CONFIRMACION = "BORRAR"


@vista.route("/")
def index():
    return render_template("index.html")


@vista.route("/calcular_cuota", methods=["POST"])
def calcular_cuota():
    try:
        nombre = request.form["nombre"].strip()
        valor_inmueble = float(request.form["valor_inmueble"])
        porcentaje = float(request.form["porcentaje"]) / 100
        tasa_mensual = float(request.form["tasa_mensual"]) / 100
        plazo_meses = int(request.form["plazo_meses"])

        datos = ParametrosHipoteca(valor_inmueble, porcentaje, tasa_mensual, plazo_meses)
        cuota, total_abonos, total_intereses = desembolso_mensual(datos)

        consulta = Consulta(nombre, valor_inmueble, porcentaje, tasa_mensual,
                            plazo_meses, cuota, total_abonos, total_intereses)
        ConsultasController.insertar(consulta)

        return render_template("resultado.html", consulta=consulta)
    except HipotecaInversaError as error:
        return render_template("error.html", mensaje=error)
    except ValueError:
        return render_template("error.html", mensaje="Ingrese solo números en todos los campos.")
    except Exception as error:
        return render_template("error.html", mensaje=f"Error inesperado: {error}")


@vista.route("/consultas")
def ver_consultas():
    nombre_buscado = request.args.get("buscar", "")
    consultas = ConsultasController.buscar(nombre_buscado)
    return render_template("consultas.html", consultas=consultas, buscar=nombre_buscado)


@vista.route("/eliminar_consulta")
def eliminar_consulta():
    ConsultasController.eliminar(request.args["id"])
    return ver_consultas()


@vista.route("/borrar_tabla")
def borrar_tabla():
    if request.args["confirmacion"] != PALABRA_CONFIRMACION:
        return render_template("error.html",
                               mensaje=f"No se borró nada. Debe escribir {PALABRA_CONFIRMACION}.")
    ConsultasController.borrar_tabla()
    return ver_consultas()
