"""Pruebas unitarias para la calculadora de impuestos."""

import unittest

from src.model import impuestos_logic


class TestImpuestos(unittest.TestCase):

    def test_calcula_iva_19_para_compra_valida(self) -> None:
        valor_total, impuesto = impuestos_logic.calcular_impuesto(
            categoria=impuestos_logic.IVA_19,
            precio_unitario=50000,
            cantidad=2,
        )

        self.assertEqual(100000, valor_total)
        self.assertEqual(19000, impuesto)

    def test_calcula_inc_restaurantes_para_compra_valida(self) -> None:
        valor_total, impuesto = impuestos_logic.calcular_impuesto(
            categoria=impuestos_logic.INC_RESTAURANTES,
            precio_unitario=35000,
            cantidad=1,
        )

        self.assertEqual(35000, valor_total)
        self.assertEqual(2800, impuesto)

    def test_calcula_impuesto_para_bolsas_plasticas(self) -> None:
        valor_total, impuesto = impuestos_logic.calcular_impuesto(
            categoria=impuestos_logic.BOLSAS_PLASTICAS,
            precio_unitario=500,
            cantidad=7,
        )

        self.assertEqual(3500, valor_total)
        self.assertEqual(511, impuesto)

    def test_calcula_iva_5_con_precio_decimal(self) -> None:
        valor_total, impuesto = impuestos_logic.calcular_impuesto(
            categoria=impuestos_logic.IVA_5,
            precio_unitario=15499.75,
            cantidad=1,
        )

        self.assertAlmostEqual(15499.75, valor_total, places=2)
        self.assertAlmostEqual(774.9875, impuesto, places=2)

    def test_calcula_impuesto_para_valor_alto(self) -> None:
        valor_total, impuesto = impuestos_logic.calcular_impuesto(
            categoria=impuestos_logic.SUNTUARIOS,
            precio_unitario=850000000,
            cantidad=1,
        )

        self.assertEqual(850000000, valor_total)
        self.assertEqual(161500000, impuesto)

    def test_calcula_impuesto_fijo_para_una_bolsa(self) -> None:
        valor_total, impuesto = impuestos_logic.calcular_impuesto(
            categoria=impuestos_logic.BOLSAS_PLASTICAS,
            precio_unitario=500,
            cantidad=1,
        )

        self.assertEqual(500, valor_total)
        self.assertEqual(73, impuesto)

    def test_rechaza_precio_negativo(self) -> None:
        with self.assertRaises(impuestos_logic.InvalidPriceError):
            impuestos_logic.calcular_impuesto(
                categoria=impuestos_logic.IVA_19,
                precio_unitario=-50000,
                cantidad=1,
            )

    def test_rechaza_precio_no_numerico(self) -> None:
        with self.assertRaises(impuestos_logic.NonNumericPriceError):
            impuestos_logic.calcular_impuesto(
                categoria=impuestos_logic.INC_RESTAURANTES,
                precio_unitario="abc",
                cantidad=1,
            )

    def test_rechaza_cantidad_cero(self) -> None:
        with self.assertRaises(impuestos_logic.ZeroQuantityError):
            impuestos_logic.calcular_impuesto(
                categoria=impuestos_logic.BOLSAS_PLASTICAS,
                precio_unitario=500,
                cantidad=0,
            )

    def test_rechaza_cantidad_negativa(self) -> None:
        with self.assertRaises(impuestos_logic.NegativeQuantityError):
            impuestos_logic.calcular_impuesto(
                categoria=impuestos_logic.CIGARRILLOS_VAPEADORES,
                precio_unitario=15000,
                cantidad=-10,
            )

    def test_rechaza_precio_cero(self) -> None:
        with self.assertRaises(impuestos_logic.InvalidPriceError):
            impuestos_logic.calcular_impuesto(
                categoria=impuestos_logic.IVA_19,
                precio_unitario=0,
                cantidad=1,
            )

    def test_rechaza_categoria_invalida(self) -> None:
        with self.assertRaises(impuestos_logic.InvalidCategoryError):
            impuestos_logic.calcular_impuesto(
                categoria="categoria_inexistente",
                precio_unitario=50000,
                cantidad=1,
            )

    def test_rechaza_cantidad_no_numerica(self) -> None:
        with self.assertRaises(impuestos_logic.NonNumericQuantityError):
            impuestos_logic.calcular_impuesto(
                categoria=impuestos_logic.IVA_19,
                precio_unitario=50000,
                cantidad="abc",
            )


if __name__ == "__main__":
    unittest.main()