"""Interfaz gráfica en Kivy para la aplicación de hipoteca inversa.

Construida siguiendo los patrones del proyecto de ejemplo
https://github.com/ProfeBill/hello-kivy:

- ``BoxLayout`` (orientation="vertical"/"horizontal") para organizar los
  controles en filas, igual que en ``input.py``.
- ``TextInput`` para capturar los datos del usuario.
- ``Button.bind(on_press=...)`` para conectar cada botón con un callback,
  igual que en ``events.py``.
- ``Label`` para mostrar resultados y mensajes de error.

La ventana tiene tres pestañas: calcular hipoteca, registrar cliente y
buscar cliente.

Esta vista no contiene lógica de negocio ni de validación de formato:
solo recoge los datos y se los entrega a los controladores
(`src.controller.hipoteca_controller` y `src.controller.cliente_controller`),
los mismos que usa la interfaz de consola (`console.py`), y muestra el
resultado o el mensaje de error que estos le devuelvan.

Requisitos:
    pip install -r requirements.txt

Ejecución: se puede lanzar de cualquier forma (`python interfaz_kivy.py`,
`python src/view/interfaz_kivy.py`, `python -m src.view.interfaz_kivy`, o
desde el botón "Run" de un editor) gracias al ajuste de sys.path incluido
más abajo.
"""

import sys
from pathlib import Path

# Agrega la raíz del proyecto a sys.path para que `import src...` funcione
# sin importar cómo se invoque este archivo (ver detalle en console.py).
_RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
if str(_RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(_RAIZ_PROYECTO))

from kivy.app import App  # noqa: E402
from kivy.uix.boxlayout import BoxLayout  # noqa: E402
from kivy.uix.button import Button  # noqa: E402
from kivy.uix.label import Label  # noqa: E402
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem  # noqa: E402
from kivy.uix.textinput import TextInput  # noqa: E402

from src.controller import cliente_controller as clientes  # noqa: E402
from src.controller import hipoteca_controller as controlador  # noqa: E402


def _fila_de_entrada(texto_etiqueta):
    """Crea una fila horizontal con una Label y un TextInput.

    Sigue el mismo patrón de composición de widgets que ``input.py`` en
    hello-kivy: un BoxLayout agrupa los controles y se retorna también
    el TextInput para poder leer su valor más adelante.
    """
    fila = BoxLayout(orientation="horizontal", size_hint_y=None, height=48, spacing=10)
    etiqueta = Label(text=texto_etiqueta, size_hint_x=0.6, halign="left", valign="middle")
    etiqueta.bind(size=etiqueta.setter("text_size"))
    entrada = TextInput(multiline=False, size_hint_x=0.4)
    fila.add_widget(etiqueta)
    fila.add_widget(entrada)
    return fila, entrada


def _etiqueta_resultado(texto_inicial):
    """Label para mostrar resultados o mensajes de error."""
    etiqueta = Label(text=texto_inicial, halign="center", valign="middle")
    etiqueta.bind(size=etiqueta.setter("text_size"))
    return etiqueta


def _contenedor():
    return BoxLayout(orientation="vertical", padding=20, spacing=12)


class HipotecaInversaApp(App):
    """Aplicación Kivy: cada app desciende de ``kivy.app.App``."""

    title = "Hipoteca Inversa"

    def build(self):
        # build() crea y retorna el widget contenedor de toda la ventana,
        # tal como se hace en hello.py, input.py y events.py. Aquí es un
        # TabbedPanel: la pestaña por defecto calcula la hipoteca y se
        # agregan dos pestañas para registrar y buscar clientes.
        panel = TabbedPanel(do_default_tab=True, default_tab_text="Calcular hipoteca")
        panel.default_tab_content = self._construir_calculo()

        for titulo, contenido in (
            ("Registrar cliente", self._construir_registro()),
            ("Buscar cliente", self._construir_busqueda()),
        ):
            pestana = TabbedPanelItem(text=titulo)
            pestana.add_widget(contenido)
            panel.add_widget(pestana)

        return panel

    # ------------------------------------------------------------------
    # Pestaña 1: calcular hipoteca
    # ------------------------------------------------------------------
    def _construir_calculo(self):
        contenedor = _contenedor()

        contenedor.add_widget(Label(
            text="Calculadora de Hipoteca Inversa",
            font_size=24,
            size_hint_y=None,
            height=40,
        ))

        fila_valor, self.entrada_valor = _fila_de_entrada("Valor del inmueble:")
        fila_porcentaje, self.entrada_porcentaje = _fila_de_entrada("Porcentaje de desembolso (%):")
        fila_tasa, self.entrada_tasa = _fila_de_entrada("Tasa de interés mensual (%):")
        fila_plazo, self.entrada_plazo = _fila_de_entrada("Plazo en meses:")

        for fila in (fila_valor, fila_porcentaje, fila_tasa, fila_plazo):
            contenedor.add_widget(fila)

        boton_calcular = Button(text="Calcular", size_hint_y=None, height=56)
        # bind(on_press=...) conecta el evento del botón con el callback,
        # igual que Boton.bind(on_press=self.callback) en events.py.
        boton_calcular.bind(on_press=self.calcular)
        contenedor.add_widget(boton_calcular)

        self.resultado = _etiqueta_resultado("Ingrese los datos y presione Calcular.")
        contenedor.add_widget(self.resultado)

        return contenedor

    def calcular(self, instance):
        """Callback del botón Calcular.

        ``instance`` es el widget que generó el evento (el propio botón),
        siguiendo la misma convención de ``seleccionar_casilla`` en
        tictactoe.py. Todo el trabajo de conversión de datos, validación
        de negocio y manejo de errores vive en el controlador, que es el
        mismo que usa la consola: esta vista solo lee los TextInput y
        escribe el resultado.
        """
        try:
            resultado = controlador.calcular_hipoteca(
                self.entrada_valor.text,
                self.entrada_porcentaje.text,
                self.entrada_tasa.text,
                self.entrada_plazo.text,
            )
        except controlador.ErrorCalculoHipoteca as error:
            self.resultado.text = str(error)
            return

        self.resultado.text = (
            f"Cuota mensual: {resultado.cuota_mensual:,.2f}\n"
            f"Total abonos: {resultado.total_abonos:,.2f}\n"
            f"Total intereses: {resultado.total_intereses:,.2f}"
        )

    # ------------------------------------------------------------------
    # Pestaña 2: registrar cliente (insertar datos)
    # ------------------------------------------------------------------
    def _construir_registro(self):
        contenedor = _contenedor()

        fila_cedula, self.reg_cedula = _fila_de_entrada("Cédula:")
        fila_nombres, self.reg_nombres = _fila_de_entrada("Nombres:")
        fila_apellidos, self.reg_apellidos = _fila_de_entrada("Apellidos:")
        fila_nacimiento, self.reg_nacimiento = _fila_de_entrada("Nacimiento (AAAA-MM-DD):")
        fila_telefono, self.reg_telefono = _fila_de_entrada("Teléfono:")
        fila_direccion, self.reg_direccion = _fila_de_entrada("Dirección:")

        self._campos_registro = (
            self.reg_cedula, self.reg_nombres, self.reg_apellidos,
            self.reg_nacimiento, self.reg_telefono, self.reg_direccion,
        )

        for fila in (fila_cedula, fila_nombres, fila_apellidos,
                     fila_nacimiento, fila_telefono, fila_direccion):
            contenedor.add_widget(fila)

        boton_guardar = Button(text="Guardar cliente", size_hint_y=None, height=56)
        boton_guardar.bind(on_press=self.guardar_cliente)
        contenedor.add_widget(boton_guardar)

        self.resultado_registro = _etiqueta_resultado(
            "Complete los datos y presione Guardar cliente."
        )
        contenedor.add_widget(self.resultado_registro)

        return contenedor

    def guardar_cliente(self, instance):
        """Callback del botón Guardar cliente: delega todo en el controlador."""
        try:
            cliente = clientes.insertar_cliente(
                self.reg_cedula.text,
                self.reg_nombres.text,
                self.reg_apellidos.text,
                self.reg_nacimiento.text,
                self.reg_telefono.text,
                self.reg_direccion.text,
            )
        except clientes.ErrorCliente as error:
            self.resultado_registro.text = str(error)
            return

        self.resultado_registro.text = f"Cliente guardado con id {cliente.id_cliente}."
        for campo in self._campos_registro:
            campo.text = ""

    # ------------------------------------------------------------------
    # Pestaña 3: buscar cliente (consultar datos)
    # ------------------------------------------------------------------
    def _construir_busqueda(self):
        contenedor = _contenedor()

        fila_cedula, self.bus_cedula = _fila_de_entrada("Buscar por cédula:")
        boton_cedula = Button(text="Buscar por cédula", size_hint_y=None, height=48)
        boton_cedula.bind(on_press=self.buscar_por_cedula)

        fila_texto, self.bus_texto = _fila_de_entrada("Buscar por nombre o apellido:")
        boton_texto = Button(text="Buscar por nombre o apellido", size_hint_y=None, height=48)
        boton_texto.bind(on_press=self.buscar_por_texto)

        for widget in (fila_cedula, boton_cedula, fila_texto, boton_texto):
            contenedor.add_widget(widget)

        self.resultado_busqueda = _etiqueta_resultado(
            "Escriba una cédula o un nombre y presione el botón de búsqueda."
        )
        contenedor.add_widget(self.resultado_busqueda)

        return contenedor

    def buscar_por_cedula(self, instance):
        try:
            cliente = clientes.buscar_cliente_por_cedula(self.bus_cedula.text)
        except clientes.ErrorCliente as error:
            self.resultado_busqueda.text = str(error)
            return

        if cliente is None:
            self.resultado_busqueda.text = "No se encontró ningún cliente con esa cédula."
        else:
            self.resultado_busqueda.text = clientes.formatear_cliente(cliente)

    def buscar_por_texto(self, instance):
        try:
            encontrados = clientes.buscar_clientes(self.bus_texto.text)
        except clientes.ErrorCliente as error:
            self.resultado_busqueda.text = str(error)
            return

        if not encontrados:
            self.resultado_busqueda.text = "No se encontraron clientes."
            return

        self.resultado_busqueda.text = "\n\n".join(
            clientes.formatear_cliente(cliente) for cliente in encontrados
        )


if __name__ == "__main__":
    HipotecaInversaApp().run()
