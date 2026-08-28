"""Pruebas unitarias para la calculadora de impuestos."""

import unittest

from src.model import impuestos_logic


class TestImpuestos(unittest.TestCase):

    def test_calcula_iva_19_para_compra_valida(self) -> None:
        compra = impuestos_logic.Compra(
            categoria=impuestos_logic.IVA_19,
            precio_unitario=50000,
            cantidad=2,
        )

        valor_total, impuesto = impuestos_logic.calcular_impuesto(
            compra=compra
        )

        self.assertEqual(100000, valor_total)
        self.assertEqual(19000, impuesto)

    def test_calcula_inc_restaurantes_para_compra_valida(self) -> None:
        compra = impuestos_logic.Compra(
            categoria=impuestos_logic.INC_RESTAURANTES,
            precio_unitario=35000,
            cantidad=1,
        )

        valor_total, impuesto = impuestos_logic.calcular_impuesto(
            compra=compra
        )

        self.assertEqual(35000, valor_total)
        self.assertEqual(2800, impuesto)

    def test_calcula_impuesto_para_bolsas_plasticas(self) -> None:
        compra = impuestos_logic.Compra(
            categoria=impuestos_logic.BOLSAS_PLASTICAS,
            precio_unitario=500,
            cantidad=7,
        )

        valor_total, impuesto = impuestos_logic.calcular_impuesto(
            compra=compra
        )

        self.assertEqual(3500, valor_total)
        self.assertEqual(511, impuesto)

    def test_calcula_iva_5_con_precio_decimal(self) -> None:
        compra = impuestos_logic.Compra(
            categoria=impuestos_logic.IVA_5,
            precio_unitario=15499.75,
            cantidad=1,
        )

        valor_total, impuesto = impuestos_logic.calcular_impuesto(
            compra=compra
        )

        self.assertAlmostEqual(15499.75, valor_total, places=2)
        self.assertAlmostEqual(774.9875, impuesto, places=2)

    def test_calcula_impuesto_para_valor_alto(self) -> None:
        compra = impuestos_logic.Compra(
            categoria=impuestos_logic.SUNTUARIOS,
            precio_unitario=850000000,
            cantidad=1,
        )

        valor_total, impuesto = impuestos_logic.calcular_impuesto(
            compra=compra
        )

        self.assertEqual(850000000, valor_total)
        self.assertEqual(161500000, impuesto)

    def test_calcula_impuesto_fijo_para_una_bolsa(self) -> None:
        compra = impuestos_logic.Compra(
            categoria=impuestos_logic.BOLSAS_PLASTICAS,
            precio_unitario=500,
            cantidad=1,
        )

        valor_total, impuesto = impuestos_logic.calcular_impuesto(
            compra=compra
        )

        self.assertEqual(500, valor_total)
        self.assertEqual(73, impuesto)

    def test_rechaza_precio_negativo(self) -> None:
        compra = impuestos_logic.Compra(
            categoria=impuestos_logic.IVA_19,
            precio_unitario=-50000,
            cantidad=1,
        )

        with self.assertRaises(impuestos_logic.InvalidPriceError):
            impuestos_logic.calcular_impuesto(compra=compra)

    def test_rechaza_precio_no_numerico(self) -> None:
        compra = impuestos_logic.Compra(
            categoria=impuestos_logic.INC_RESTAURANTES,
            precio_unitario="abc",
            cantidad=1,
        )

        with self.assertRaises(impuestos_logic.NonNumericPriceError):
            impuestos_logic.calcular_impuesto(compra=compra)

    def test_rechaza_cantidad_cero(self) -> None:
        compra = impuestos_logic.Compra(
            categoria=impuestos_logic.BOLSAS_PLASTICAS,
            precio_unitario=500,
            cantidad=0,
        )

        with self.assertRaises(impuestos_logic.ZeroQuantityError):
            impuestos_logic.calcular_impuesto(compra=compra)

    def test_rechaza_cantidad_negativa(self) -> None:
        compra = impuestos_logic.Compra(
            categoria=impuestos_logic.CIGARRILLOS_VAPEADORES,
            precio_unitario=15000,
            cantidad=-10,
        )

        with self.assertRaises(impuestos_logic.NegativeQuantityError):
            impuestos_logic.calcular_impuesto(compra=compra)

    def test_rechaza_precio_cero(self) -> None:
        compra = impuestos_logic.Compra(
            categoria=impuestos_logic.IVA_19,
            precio_unitario=0,
            cantidad=1,
        )

        with self.assertRaises(impuestos_logic.InvalidPriceError):
            impuestos_logic.calcular_impuesto(compra=compra)

    def test_rechaza_categoria_invalida(self) -> None:
        compra = impuestos_logic.Compra(
            categoria="categoria_inexistente",
            precio_unitario=50000,
            cantidad=1,
        )

        with self.assertRaises(impuestos_logic.InvalidCategoryError):
            impuestos_logic.calcular_impuesto(compra=compra)

    def test_rechaza_cantidad_no_numerica(self) -> None:
        compra = impuestos_logic.Compra(
            categoria=impuestos_logic.IVA_19,
            precio_unitario=50000,
            cantidad="abc",
        )

        with self.assertRaises(impuestos_logic.NonNumericQuantityError):
            impuestos_logic.calcular_impuesto(compra=compra)


if __name__ == "__main__":
    unittest.main()