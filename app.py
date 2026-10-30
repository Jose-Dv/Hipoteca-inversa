"""Servidor local de la aplicación web. Ejecutar con: python app.py"""

import sys
sys.path.append("src")

from flask import Flask, render_template, request

from model.logica_hipoteca_inversa import ParametrosHipoteca, desembolso_mensual, HipotecaInversaError
from model.consulta import Consulta
from controller.consultas_controller import ConsultasController

app = Flask(__name__)


@app.route("/")
def index():
    nombre_buscado = request.args.get("buscar", "")
    consultas = ConsultasController.buscar(nombre_buscado)
    return render_template("index.html", consultas=consultas, buscar=nombre_buscado)


@app.route("/calcular_cuota", methods=["POST"])
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

        ConsultasController.insertar(Consulta(
            nombre, valor_inmueble, porcentaje, tasa_mensual, plazo_meses,
            cuota, total_abonos, total_intereses,
        ))

        return (
            f"<h3>Resultados del Cálculo</h3>"
            f"<p>Desembolso Mensual: {cuota:,.2f}<br>"
            f"Total Abonos: {total_abonos:,.2f}<br>"
            f"Total Intereses: {total_intereses:,.2f}</p>"
            f'<a href="/">Volver</a>'
        )
    except HipotecaInversaError as error:
        return f'<h3>Error de Validación</h3><p>{error}</p><a href="/">Volver</a>', 400
    except ValueError:
        return '<h3>Error</h3><p>Ingrese solo números en todos los campos.</p><a href="/">Volver</a>', 400
    except Exception as error:
        return f'<h3>Error inesperado</h3><p>{error}</p><a href="/">Volver</a>', 500


if __name__ == "__main__":
    app.run(debug=True)
