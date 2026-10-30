"""Pruebas unitarias del cálculo de desembolso mensual de la hipoteca inversa."""

import unittest
from src.model import logica_hipoteca_inversa


class TestHipoteca(unittest.TestCase):
    """Casos normales, extraordinarios y de error de ``desembolso_mensual``."""

    # Casos normales
    def test_normal_1(self):
        """Inmueble de 300 millones, 40 % financiado, 1.2 % mensual, 120 meses."""
        valor_inmueble = 300_000_000
        porcentaje = 0.40
        tasa_mensual = 0.012
        plazo_meses = 120

        cuota_esperada = 1892165.77
        abonos_esperado = 227059892.25
        intereses_esperado = 107059892.25

        parametros = logica_hipoteca_inversa.ParametrosHipoteca(
            valor_inmueble, porcentaje, tasa_mensual, plazo_meses
        )
        cuota, abonos, intereses = logica_hipoteca_inversa.desembolso_mensual(parametros)

        self.assertAlmostEqual(cuota, cuota_esperada, places=2)
        self.assertAlmostEqual(abonos, abonos_esperado, places=2)
        self.assertAlmostEqual(intereses, intereses_esperado, places=2)

    def test_normal_2(self):
        """Inmueble de 150 millones, 50 % financiado, 0.9 % mensual, 60 meses."""
        valor_inmueble = 150_000_000
        porcentaje = 0.50
        tasa_mensual = 0.009
        plazo_meses = 60

        cuota_esperada = 1623211.07
        abonos_esperado = 97392664.32
        intereses_esperado = 22392664.32

        parametros = logica_hipoteca_inversa.ParametrosHipoteca(
            valor_inmueble, porcentaje, tasa_mensual, plazo_meses
        )
        cuota, abonos, intereses = logica_hipoteca_inversa.desembolso_mensual(parametros)

        self.assertAlmostEqual(cuota, cuota_esperada, places=2)
        self.assertAlmostEqual(abonos, abonos_esperado, places=2)
        self.assertAlmostEqual(intereses, intereses_esperado, places=2)

    def test_normal_3(self):
        """Inmueble de 500 millones, 30 % financiado, 1.5 % mensual, 48 meses."""
        valor_inmueble = 500_000_000
        porcentaje = 0.30
        tasa_mensual = 0.015
        plazo_meses = 48

        cuota_esperada = 4406249.94
        abonos_esperado = 211499997.18
        intereses_esperado = 61499997.18

        parametros = logica_hipoteca_inversa.ParametrosHipoteca(
            valor_inmueble, porcentaje, tasa_mensual, plazo_meses
        )
        cuota, abonos, intereses = logica_hipoteca_inversa.desembolso_mensual(parametros)

        self.assertAlmostEqual(cuota, cuota_esperada, places=2)
        self.assertAlmostEqual(abonos, abonos_esperado, places=2)
        self.assertAlmostEqual(intereses, intereses_esperado, places=2)

    # Casos extraordinarios
    def test_extraordinario_tasa_cero(self):
        """Con tasa cero no hay intereses: el valor financiado se divide en cuotas iguales."""
        valor_inmueble = 200_000_000
        porcentaje = 0.50
        tasa_mensual = 0.0
        plazo_meses = 36

        cuota_esperada = 2777777.78
        abonos_esperado = 100000000.00
        intereses_esperado = 0.00

        parametros = logica_hipoteca_inversa.ParametrosHipoteca(
            valor_inmueble, porcentaje, tasa_mensual, plazo_meses
        )
        cuota, abonos, intereses = logica_hipoteca_inversa.desembolso_mensual(parametros)

        self.assertAlmostEqual(cuota, cuota_esperada, places=2)
        self.assertAlmostEqual(abonos, abonos_esperado, places=2)
        self.assertAlmostEqual(intereses, intereses_esperado, places=2)

    def test_extraordinario_unica_disposicion(self):
        """Con 100 % financiado y un solo mes, se paga todo el capital más un mes de interés."""
        valor_inmueble = 100_000_000
        porcentaje = 1.00
        tasa_mensual = 0.024
        plazo_meses = 1

        cuota_esperada = 102400000.00
        abonos_esperado = 102400000.00
        intereses_esperado = 2400000.00

        parametros = logica_hipoteca_inversa.ParametrosHipoteca(
            valor_inmueble, porcentaje, tasa_mensual, plazo_meses
        )
        cuota, abonos, intereses = logica_hipoteca_inversa.desembolso_mensual(parametros)

        self.assertAlmostEqual(cuota, cuota_esperada, places=2)
        self.assertAlmostEqual(abonos, abonos_esperado, places=2)
        self.assertAlmostEqual(intereses, intereses_esperado, places=2)

    def test_extraordinario_plazo_maximo(self):
        """Con el plazo máximo permitido (240 meses) el cálculo sigue siendo válido."""
        valor_inmueble = 250_000_000
        porcentaje = 0.40
        tasa_mensual = 0.018
        plazo_meses = 240

        cuota_esperada = 1825226
        abonos_esperado = 438054262
        intereses_esperado = 338054262

        parametros = logica_hipoteca_inversa.ParametrosHipoteca(
            valor_inmueble, porcentaje, tasa_mensual, plazo_meses
        )
        cuota, abonos, intereses = logica_hipoteca_inversa.desembolso_mensual(parametros)

        self.assertAlmostEqual(cuota, cuota_esperada, places=0)
        self.assertAlmostEqual(abonos, abonos_esperado, places=0)
        self.assertAlmostEqual(intereses, intereses_esperado, places=0)

    # Casos de error
    def test_error_valor_inmueble_cero(self):
        """Un inmueble de valor cero lanza ValorPropiedadCero."""
        parametros = logica_hipoteca_inversa.ParametrosHipoteca(0, 0.40, 0.012, 60)
        with self.assertRaises(logica_hipoteca_inversa.ValorPropiedadCero):
            logica_hipoteca_inversa.desembolso_mensual(parametros)

    def test_error_tasa_usura(self):
        """Una tasa mensual de 5 % supera el límite de usura y lanza HipotecaUsura."""
        parametros = logica_hipoteca_inversa.ParametrosHipoteca(200_000_000, 0.50, 0.05, 36)
        with self.assertRaises(logica_hipoteca_inversa.HipotecaUsura):
            logica_hipoteca_inversa.desembolso_mensual(parametros)

    def test_error_plazo_cero(self):
        """Un plazo de cero meses lanza PlazoMenorIgualCero."""
        parametros = logica_hipoteca_inversa.ParametrosHipoteca(150_000_000, 0.30, 0.012, 0)
        with self.assertRaises(logica_hipoteca_inversa.PlazoMenorIgualCero):
            logica_hipoteca_inversa.desembolso_mensual(parametros)

    def test_error_plazo_mayor_240(self):
        """Un plazo de 250 meses supera el máximo y lanza PlazoMayorPermitido."""
        parametros = logica_hipoteca_inversa.ParametrosHipoteca(150_000_000, 0.30, 0.012, 250)
        with self.assertRaises(logica_hipoteca_inversa.PlazoMayorPermitido):
            logica_hipoteca_inversa.desembolso_mensual(parametros)


if __name__ == "__main__":
    unittest.main()
