"""Pruebas de guardar, buscar y eliminar consultas en la base de datos.

ADVERTENCIA: el fixture borra y recrea la tabla ``consultas`` de la base
configurada en ``secret_config.py``.
"""

import sys
sys.path.append("src")

import unittest

from model.consulta import Consulta
from controller.consultas_controller import ConsultasController


class TestConsultasController(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """Test fixture: crea la tabla una sola vez, al inicio de las pruebas."""
        ConsultasController.borrar_tabla()
        ConsultasController.crear_tabla()

    def test_insertar_1_consulta_con_nombre(self) -> None:
        consulta = Consulta("Ana Prueba Uno", 300_000_000, 0.40, 0.012, 120,
                            1892165.77, 227059892.25, 107059892.25)

        ConsultasController.insertar(consulta)
        encontradas = ConsultasController.buscar("Ana Prueba Uno")

        self.assertEqual(encontradas, [consulta])

    def test_insertar_2_consulta_sin_nombre(self) -> None:
        consulta = Consulta("", 150_000_000, 0.50, 0.009, 60,
                            1623211.07, 97392664.32, 22392664.32)

        ConsultasController.insertar(consulta)

        self.assertIn(consulta, ConsultasController.buscar(""))

    def test_buscar_3_por_parte_del_nombre_sin_distinguir_mayusculas(self) -> None:
        consulta = Consulta("Carlos Zapata", 500_000_000, 0.30, 0.015, 48,
                            4406249.94, 211499997.18, 61499997.18)

        ConsultasController.insertar(consulta)
        encontradas = ConsultasController.buscar("zapata")

        self.assertEqual(encontradas, [consulta])

    def test_buscar_4_nombre_inexistente(self) -> None:
        self.assertEqual(ConsultasController.buscar("Nombre Que No Existe"), [])

    def test_insertar_5_crea_la_tabla_si_no_existe(self) -> None:
        consulta = Consulta("Tabla Nueva", 200_000_000, 0.50, 0.0, 36,
                            2777777.78, 100000000.0, 0.0)
        ConsultasController.borrar_tabla()

        ConsultasController.insertar(consulta)

        self.assertEqual(ConsultasController.buscar("Tabla Nueva"), [consulta])

    def test_eliminar_6_una_consulta(self) -> None:
        consulta = Consulta("Para Eliminar", 100_000_000, 0.40, 0.010, 24,
                            1000000.0, 24000000.0, 1000000.0)
        ConsultasController.insertar(consulta)
        guardada = ConsultasController.buscar("Para Eliminar")[0]

        ConsultasController.eliminar(guardada.id)

        self.assertEqual(ConsultasController.buscar("Para Eliminar"), [])


if __name__ == "__main__":
    unittest.main()
