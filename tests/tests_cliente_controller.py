"""Pruebas de insertar y buscar clientes contra la base de datos.

ADVERTENCIA: el fixture borra y recrea las tablas de la base configurada en
``secret_config.py``. Úselas solo con una base de desarrollo (en Neon, una
rama de pruebas).
"""

import unittest

from src.controller import cliente_controller as controlador


class TestClienteController(unittest.TestCase):
    """Casos de insertar y buscar clientes, más validaciones de formato."""

    @classmethod
    def setUpClass(cls) -> None:
        """Test fixture: crea las tablas una sola vez, al inicio de las pruebas."""
        controlador.borrar_tablas()
        controlador.crear_tablas()

    def test_insertar_1_cliente_con_todos_los_datos(self) -> None:
        cliente_guardado = controlador.insertar_cliente(
            "1001", "Ana María", "Pérez Gómez", "1990-05-23", "3001234567", "Calle 10 # 20-30"
        )

        cliente_buscado = controlador.buscar_cliente_por_cedula("1001")

        self.assertEqual(cliente_buscado, cliente_guardado)

    def test_insertar_2_cliente_solo_con_datos_obligatorios(self) -> None:
        cliente_guardado = controlador.insertar_cliente("1002", "Luis", "Rojas")

        cliente_buscado = controlador.buscar_cliente_por_cedula("1002")

        self.assertEqual(cliente_buscado, cliente_guardado)
        self.assertIsNone(cliente_buscado.fecha_nacimiento)

    def test_buscar_cedula_inexistente(self) -> None:
        self.assertIsNone(controlador.buscar_cliente_por_cedula("999999"))

    def test_insertar_cedula_duplicada(self) -> None:
        controlador.insertar_cliente("1003", "Marta", "Díaz")

        with self.assertRaises(controlador.ErrorCliente):
            controlador.insertar_cliente("1003", "Otra", "Persona")

    def test_buscar_por_nombre_o_apellido(self) -> None:
        controlador.insertar_cliente("1004", "Carlos", "Ramírez")
        controlador.insertar_cliente("1005", "Camila", "Ramos")

        cedulas_por_apellido = {cliente.cedula for cliente in controlador.buscar_clientes("RAM")}
        cedulas_por_nombre = {cliente.cedula for cliente in controlador.buscar_clientes("carlos")}

        self.assertEqual(cedulas_por_apellido, {"1004", "1005"})
        self.assertEqual(cedulas_por_nombre, {"1004"})

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
