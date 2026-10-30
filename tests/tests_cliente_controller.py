"""Pruebas de insertar y buscar clientes contra la base de datos de pruebas.

ADVERTENCIA: el fixture borra y recrea las tablas de ``DATABASE_URL_PRUEBAS``.
Esa cadena debe ser distinta de ``DATABASE_URL`` (en Neon, use otra rama).
"""

import unittest

import secret_config
from src.controller import cliente_controller as controlador


def setUpModule() -> None:  # pylint: disable=invalid-name
    """Dirige el controlador a la base de pruebas, nunca a la de la aplicación."""
    if secret_config.DATABASE_URL_PRUEBAS == secret_config.DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL_PRUEBAS debe ser distinta de DATABASE_URL: "
            "las pruebas borran las tablas."
        )
    controlador.url_base_de_datos = secret_config.DATABASE_URL_PRUEBAS


def tearDownModule() -> None:  # pylint: disable=invalid-name
    """Restablece la configuración normal del controlador."""
    controlador.url_base_de_datos = None


class TestClienteController(unittest.TestCase):
    """Casos de insertar y buscar clientes, más validaciones de formato."""

    def setUp(self) -> None:
        controlador.borrar_tablas()
        controlador.crear_tablas()

    def test_insertar_cliente_valido(self) -> None:
        cliente = controlador.insertar_cliente("1001", "Ana María", "Pérez Gómez")
        self.assertIsNotNone(cliente.id_cliente)
        self.assertEqual(cliente.cedula, "1001")

    def test_insertar_y_buscar_por_cedula(self) -> None:
        controlador.insertar_cliente("1002", "Luis", "Rojas", "1985-03-10", "3001234567", "Calle 1")
        cliente = controlador.buscar_cliente_por_cedula("1002")
        self.assertEqual(cliente.nombres, "Luis")
        self.assertEqual(cliente.fecha_nacimiento.isoformat(), "1985-03-10")

    def test_buscar_cedula_inexistente(self) -> None:
        self.assertIsNone(controlador.buscar_cliente_por_cedula("999999"))

    def test_insertar_cedula_duplicada(self) -> None:
        controlador.insertar_cliente("1003", "Marta", "Díaz")
        with self.assertRaises(controlador.ErrorCliente):
            controlador.insertar_cliente("1003", "Otra", "Persona")

    def test_buscar_por_nombre_o_apellido(self) -> None:
        controlador.insertar_cliente("1004", "Carlos", "Ramírez")
        controlador.insertar_cliente("1005", "Camila", "Ramos")
        self.assertEqual(len(controlador.buscar_clientes("RAM")), 2)
        self.assertEqual(len(controlador.buscar_clientes("carlos")), 1)

    def test_validacion_cedula_con_letras(self) -> None:
        with self.assertRaises(controlador.ErrorCliente):
            controlador.insertar_cliente("12ab", "Ana", "Pérez")

    def test_validacion_nombres_vacios(self) -> None:
        with self.assertRaises(controlador.ErrorCliente):
            controlador.insertar_cliente("1006", "  ", "Pérez")

    def test_validacion_fecha_con_formato_invalido(self) -> None:
        with self.assertRaises(controlador.ErrorCliente):
            controlador.insertar_cliente("1007", "Ana", "Pérez", "10/03/1985")

    def test_validacion_fecha_futura(self) -> None:
        with self.assertRaises(controlador.ErrorCliente):
            controlador.insertar_cliente("1008", "Ana", "Pérez", "2999-01-01")


if __name__ == "__main__":
    unittest.main()
