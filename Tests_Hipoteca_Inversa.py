import unittest
from Logica_Hipoteca_Inversa import desembolso_mensual

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


if __name__ == "__main__":
    unittest.main()

