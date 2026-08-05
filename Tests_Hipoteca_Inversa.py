import unittest
from Logica_Hipoteca_Inversa import desembolso_mensual, HipotecaInversaError


class TestHipoteca(unittest.TestCase):

    def test_normal_1(self):
        # entradas
        valor_inmueble = 300_000_000
        porcentaje = 0.40
        tasa_mensual = 0.012
        plazo_meses = 120

        # salidas
        cuota_esperada = 1892165.77
        abonos_esperado = 227059892.25
        intereses_esperado = 107059892.25

        cuota, abonos, intereses = desembolso_mensual(valor_inmueble, porcentaje, tasa_mensual, plazo_meses)

        self.assertAlmostEqual(cuota, cuota_esperada, places=2)
        self.assertAlmostEqual(abonos, abonos_esperado, places=2)
        self.assertAlmostEqual(intereses, intereses_esperado, places=2)

    def test_normal_2(self):
        # entradas
        valor_inmueble = 150_000_000
        porcentaje = 0.50
        tasa_mensual = 0.009
        plazo_meses = 60

        # salidas
        cuota_esperada = 1623211.07
        abonos_esperado = 97392664.32
        intereses_esperado = 22392664.32

        cuota, abonos, intereses = desembolso_mensual(valor_inmueble, porcentaje, tasa_mensual, plazo_meses)

        self.assertAlmostEqual(cuota, cuota_esperada, places=2)
        self.assertAlmostEqual(abonos, abonos_esperado, places=2)
        self.assertAlmostEqual(intereses, intereses_esperado, places=2)

    def test_normal_3(self):
        # entradas
        valor_inmueble = 500_000_000
        porcentaje = 0.30
        tasa_mensual = 0.015
        plazo_meses = 48

        # salidas
        cuota_esperada = 4406249.94
        abonos_esperado = 211499997.18
        intereses_esperado = 61499997.18

        cuota, abonos, intereses = desembolso_mensual(valor_inmueble, porcentaje, tasa_mensual, plazo_meses)

        self.assertAlmostEqual(cuota, cuota_esperada, places=2)
        self.assertAlmostEqual(abonos, abonos_esperado, places=2)
        self.assertAlmostEqual(intereses, intereses_esperado, places=2)

    def test_extraordinario_1_tasa_cero(self):
        # entradas
        valor_inmueble = 200_000_000
        porcentaje = 0.50
        tasa_mensual = 0.0
        plazo_meses = 36

        # salidas
        cuota_esperada = 2777777.78
        abonos_esperado = 100000000.00
        intereses_esperado = 0.00

        cuota, abonos, intereses = desembolso_mensual(valor_inmueble, porcentaje, tasa_mensual, plazo_meses)

        self.assertAlmostEqual(cuota, cuota_esperada, places=2)
        self.assertAlmostEqual(abonos, abonos_esperado, places=2)
        self.assertAlmostEqual(intereses, intereses_esperado, places=2)

    def test_extraordinario_2_unica_disposicion(self):
        # entradas
        valor_inmueble = 100_000_000
        porcentaje = 1.00
        tasa_mensual = 0.024
        plazo_meses = 1

        # salidas
        cuota_esperada = 102400000.00
        abonos_esperado = 102400000.00
        intereses_esperado = 2400000.00

        cuota, abonos, intereses = desembolso_mensual(valor_inmueble, porcentaje, tasa_mensual, plazo_meses)

        self.assertAlmostEqual(cuota, cuota_esperada, places=2)
        self.assertAlmostEqual(abonos, abonos_esperado, places=2)
        self.assertAlmostEqual(intereses, intereses_esperado, places=2)

    def test_extraordinario_3_plazo_60(self):
        # entradas
        valor_inmueble = 250_000_000
        porcentaje = 0.40
        tasa_mensual = 0.018
        plazo_meses = 60

        # salidas calculadas con la formula de anualidad
        cuota_esperada = 2739196.64
        abonos_esperado = 164351798.40
        intereses_esperado = 64351798.40

        cuota, abonos, intereses = desembolso_mensual(valor_inmueble, porcentaje, tasa_mensual, plazo_meses)

        self.assertAlmostEqual(cuota, cuota_esperada, places=2)
        self.assertAlmostEqual(abonos, abonos_esperado, places=2)
        self.assertAlmostEqual(intereses, intereses_esperado, places=2)

    def test_error_1_valor_inmueble_cero(self):
        # entradas
        valor_inmueble = 0
        porcentaje = 0.40
        tasa_mensual = 0.012
        plazo_meses = 60

        with self.assertRaises(HipotecaInversaError) as contexto:
            desembolso_mensual(valor_inmueble, porcentaje, tasa_mensual, plazo_meses)

        self.assertIn("Valor del inmueble invalido", str(contexto.exception))

    def test_error_2_tasa_usura(self):
        # entradas
        valor_inmueble = 200_000_000
        porcentaje = 0.50
        tasa_mensual = 0.05
        plazo_meses = 36

        with self.assertRaises(HipotecaInversaError) as contexto:
            desembolso_mensual(valor_inmueble, porcentaje, tasa_mensual, plazo_meses)

        self.assertIn("Tasa mensual invalida", str(contexto.exception))

    def test_error_3_plazo_cero(self):
        # entradas
        valor_inmueble = 150_000_000
        porcentaje = 0.30
        tasa_mensual = 0.012
        plazo_meses = 0

        with self.assertRaises(HipotecaInversaError) as contexto:
            desembolso_mensual(valor_inmueble, porcentaje, tasa_mensual, plazo_meses)

        self.assertIn("Plazo invalido", str(contexto.exception))

    def test_error_4_plazo_negativo(self):
        # entradas
        valor_inmueble = 150_000_000
        porcentaje = 0.30
        tasa_mensual = 0.012
        plazo_meses = -12

        with self.assertRaises(HipotecaInversaError) as contexto:
            desembolso_mensual(valor_inmueble, porcentaje, tasa_mensual, plazo_meses)

        self.assertIn("Plazo invalido", str(contexto.exception))


if __name__ == "__main__":
    unittest.main()
