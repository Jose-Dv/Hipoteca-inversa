"""Rutas de la aplicación web: inicio, resultado, consultas y borrados."""

from flask import Blueprint, redirect, render_template, request, url_for

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

        datos = ParametrosHipoteca(
            valor_inmueble=valor_inmueble,
            porcentaje=porcentaje,
            tasa_mensual=tasa_mensual,
            plazo_meses=plazo_meses,
        )
        cuota, total_abonos, total_intereses = desembolso_mensual(datos)

        consulta = Consulta(
            nombre, valor_inmueble, porcentaje, tasa_mensual, plazo_meses,
            cuota, total_abonos, total_intereses,
        )
        ConsultasController.insertar(consulta)

        return render_template("resultado.html", consulta=consulta)
    except HipotecaInversaError as error:
        return f'<h3>Error de Validación</h3><p>{error}</p><a href="/">Volver</a>', 400
    except ValueError:
        return (
            "<h3>Error</h3><p>Ingrese solo números en todos los campos.</p>"
            '<a href="/">Volver</a>'
        ), 400
    except Exception as error:
        return f'<h3>Error inesperado</h3><p>{error}</p><a href="/">Volver</a>', 500


@vista.route("/consultas")
def ver_consultas():
    nombre_buscado = request.args.get("buscar", "")
    consultas = ConsultasController.buscar(nombre_buscado)
    return render_template("consultas.html", consultas=consultas, buscar=nombre_buscado)


@vista.route("/eliminar_consulta/<int:id_consulta>", methods=["POST"])
def eliminar_consulta(id_consulta):
    ConsultasController.eliminar(id_consulta)
    return redirect(url_for("vista.ver_consultas"))


@vista.route("/borrar_tabla", methods=["POST"])
def borrar_tabla():
    if request.form.get("confirmacion", "").strip() != PALABRA_CONFIRMACION:
        return (
            "<h3>No se borró nada</h3>"
            f"<p>Para borrar la tabla debe escribir {PALABRA_CONFIRMACION}.</p>"
            '<a href="/consultas">Volver</a>'
        ), 400

    ConsultasController.borrar_tabla()
    return redirect(url_for("vista.ver_consultas"))
