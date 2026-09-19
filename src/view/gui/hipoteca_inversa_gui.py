from __future__ import annotations

import sys
from pathlib import Path

# Permite ejecutar este archivo directamente (clic en "Run" del IDE) sin
# depender de que el usuario lance el proyecto como módulo desde la raíz.
_RAIZ_PROYECTO = Path(__file__).resolve().parents[3]
if str(_RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(_RAIZ_PROYECTO))

from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

from src.model import logica_hipoteca_inversa
from src.model.logica_hipoteca_inversa import (
    HipotecaInversaError,
    ParametrosHipoteca,
    calcular_monto_prestamo,
)

Config.set("kivy", "window_icon", "assets/icono.ico")

COLOR_CAMPO_NORMAL = (1, 1, 1, 1)
COLOR_CAMPO_ERROR = (1, 0.85, 0.85, 1)


class CampoInvalido(Exception):
    """Error de FORMATO en un campo del formulario (no es un error de negocio).

    Guarda una referencia al widget para poder resaltarlo visualmente.
    """

    def __init__(self, nombre_campo: str, widget: TextInput) -> None:
        self.widget = widget
        super().__init__(
            f"El campo '{nombre_campo}' es obligatorio y debe ser numérico."
        )


KV = """
<CampoEntrada@BoxLayout>:
    orientation: "vertical"
    size_hint_y: None
    height: "64dp"
    etiqueta: ""
    texto_ayuda: ""

    Label:
        text: root.etiqueta
        size_hint_y: None
        height: "20dp"
        halign: "left"
        text_size: self.size
        color: 0.2, 0.2, 0.2, 1

    TextInput:
        id: entrada
        multiline: False
        input_filter: "float"
        hint_text: root.texto_ayuda
        background_color: 1, 1, 1, 1
        on_text_validate: app.root.calcular()
        on_text: self.background_color = (1, 1, 1, 1)


PantallaHipoteca:

<PantallaHipoteca>:
    valor_inmueble: campo_valor.ids.entrada
    porcentaje: campo_porcentaje.ids.entrada
    tasa: campo_tasa.ids.entrada
    plazo: campo_plazo.ids.entrada

    orientation: "vertical"
    padding: "20dp"
    spacing: "10dp"
    canvas.before:
        Color:
            rgba: 0.97, 0.97, 0.99, 1
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "Calculadora de Hipoteca Inversa"
        font_size: "22sp"
        size_hint_y: None
        height: "44dp"
        bold: True
        color: 0.15, 0.15, 0.35, 1

    CampoEntrada:
        id: campo_valor
        etiqueta: "Valor del inmueble ($)"
        texto_ayuda: "Ej: 300000000"

    CampoEntrada:
        id: campo_porcentaje
        etiqueta: "Porcentaje de desembolso (%)"
        texto_ayuda: "Ej: 60"

    CampoEntrada:
        id: campo_tasa
        etiqueta: "Tasa de interés mensual (%)"
        texto_ayuda: "Ej: 1.2 (máx. 4%)"

    CampoEntrada:
        id: campo_plazo
        etiqueta: "Plazo en meses"
        texto_ayuda: "Ej: 180 (máx. 240)"

    BoxLayout:
        size_hint_y: None
        height: "48dp"
        spacing: "10dp"

        Button:
            text: "Calcular"
            bold: True
            background_color: 0.25, 0.5, 0.85, 1
            on_release: root.calcular()

        Button:
            text: "Limpiar"
            background_color: 0.7, 0.7, 0.7, 1
            on_release: root.limpiar()

    Label:
        id: etiqueta_error
        text: root.mensaje_error
        color: 0.75, 0.1, 0.1, 1
        size_hint_y: None
        height: "40dp"
        text_size: self.size
        halign: "left"
        valign: "top"

    BoxLayout:
        orientation: "vertical"
        padding: "10dp"
        canvas.before:
            Color:
                rgba: 0.90, 0.93, 0.98, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: root.resultado_texto
            text_size: self.width, None
            halign: "left"
            valign: "top"
            color: 0,0,0,1
"""


class PantallaHipoteca(BoxLayout):
    """Pantalla principal: captura datos, valida formato y muestra resultados."""

    mensaje_error = StringProperty("")
    resultado_texto = StringProperty("Los resultados aparecerán aquí.")

    # -- Acciones disparadas desde la interfaz -----------------------------

    def calcular(self) -> None:
        """Orquesta lectura, validación de formato, cálculo y presentación."""
        self.mensaje_error = ""

        try:
            parametros = self._leer_parametros()
        except CampoInvalido as error:
            self._mostrar_error_de_campo(error)
            return

        try:
            monto_prestamo = calcular_monto_prestamo(parametros)
            cuota, abonos, intereses = logica_hipoteca_inversa.desembolso_mensual(
                parametros
            )
        except HipotecaInversaError as error:
            self.mensaje_error = str(error)
            return

        self.resultado_texto = self._formatear_resultado(
            monto_prestamo, cuota, abonos, intereses
        )

    def limpiar(self) -> None:
        """Funcionalidad extra: restablece el formulario a su estado inicial."""
        for campo in (self.valor_inmueble, self.porcentaje, self.tasa, self.plazo):
            campo.text = ""
            campo.background_color = COLOR_CAMPO_NORMAL
        self.mensaje_error = ""
        self.resultado_texto = "Los resultados aparecerán aquí."

    # -- Lectura y validación de formato de entrada -------------------------

    def _leer_parametros(self) -> ParametrosHipoteca:
        """Convierte el texto de los campos a `ParametrosHipoteca`.

        Raises:
            CampoInvalido: si algún campo está vacío o no es numérico.
        """
        valor_inmueble = self._leer_campo_numerico(
            self.valor_inmueble, "Valor del inmueble"
        )
        porcentaje = self._leer_campo_numerico(
            self.porcentaje, "Porcentaje de desembolso"
        ) / 100
        tasa_mensual = self._leer_campo_numerico(
            self.tasa, "Tasa de interés mensual"
        ) / 100
        plazo_meses = int(self._leer_campo_numerico(self.plazo, "Plazo en meses"))

        return ParametrosHipoteca(
            valor_inmueble=valor_inmueble,
            porcentaje=porcentaje,
            tasa_mensual=tasa_mensual,
            plazo_meses=plazo_meses,
        )

    @staticmethod
    def _leer_campo_numerico(campo: TextInput, nombre_visible: str) -> float:
        """Lee y convierte el texto de un campo a `float`.

        Raises:
            CampoInvalido: si el texto está vacío o no es un número.
        """
        try:
            return float(campo.text)
        except ValueError as error:
            raise CampoInvalido(nombre_visible, campo) from error

    def _mostrar_error_de_campo(self, error: CampoInvalido) -> None:
        """Muestra el mensaje de error y resalta visualmente el campo afectado."""
        self.mensaje_error = str(error)
        error.widget.background_color = COLOR_CAMPO_ERROR

    # -- Presentación ---------------------------------------------------------

    @staticmethod
    def _formatear_resultado(
        monto_prestamo: float, cuota: float, abonos: float, intereses: float
    ) -> str:
        return (
            f"Monto del préstamo: ${monto_prestamo:,.2f}\n"
            f"Cuota mensual: ${cuota:,.2f}\n"
            f"Total abonos: ${abonos:,.2f}\n"
            f"Total intereses: ${intereses:,.2f}"
        )


class HipotecaInversaApp(App):
    def build(self):
        Builder.load_string(KV)
        return PantallaHipoteca()


if __name__ == "__main__":
    HipotecaInversaApp().run()