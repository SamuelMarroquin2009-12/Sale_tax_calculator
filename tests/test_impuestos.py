# test_impuestos.py
# Pruebas unitarias - Calculadora de Impuestos de Compra - Colombia
import sys
sys.path.append("src")

import unittest
from model import impuestos_logic
class ImpuestosTest(unittest.TestCase):
    # ---------- CASOS NORMALES ----------
    def test_normal_1(self):
        # Entradas
        categoria = impuestos_logic.IVA_19
        precio_unitario = 50000
        cantidad = 2
        # Proceso
        valor_total, impuesto = impuestos_logic.calcular_impuesto(categoria, precio_unitario, cantidad)
        # Verificacion
        self.assertEqual(100000, valor_total)
        self.assertEqual(19000, impuesto)
    def test_normal_2(self):
        categoria = impuestos_logic.INC_RESTAURANTES
        precio_unitario = 35000
        cantidad = 1
        valor_total, impuesto = impuestos_logic.calcular_impuesto(categoria, precio_unitario, cantidad)
        self.assertEqual(35000, valor_total)
        self.assertEqual(2800, impuesto)
    def test_normal_3(self):
        categoria = impuestos_logic.BOLSAS_PLASTICAS
        precio_unitario = 500
        cantidad = 7
        valor_total, impuesto = impuestos_logic.calcular_impuesto(categoria, precio_unitario, cantidad)
        self.assertEqual(3500, valor_total)
        self.assertEqual(511, impuesto)
 
    # ---------- CASOS EXTRAORDINARIOS ----------
    def test_extraordinario_1(self):
        categoria = impuestos_logic.IVA_5
        precio_unitario = 15499.75
        cantidad = 1
        valor_total, impuesto = impuestos_logic.calcular_impuesto(categoria, precio_unitario, cantidad)
        self.assertAlmostEqual(15499.75, valor_total, 2)
        self.assertAlmostEqual(774.9875, impuesto, 2)
 
    def test_extraordinario_2(self):
        # Entradas
        categoria = impuestos_logic.SUNTUARIOS
        precio_unitario = 850000000
        cantidad = 1
 
        # Funcionalidad
        valor_total, impuesto = impuestos_logic.calcular_impuesto(
            categoria,
            precio_unitario,
            cantidad
        )
 
        # Salidas Esperadas
        valor_total_esperado = 850000000
        impuesto_esperado = 161500000
 
        # Verificacion
        self.assertEqual(valor_total_esperado, valor_total)
        self.assertEqual(impuesto_esperado, impuesto)
 
    def test_extraordinario_3(self):
        # Entradas
        categoria = impuestos_logic.BOLSAS_PLASTICAS
        precio_unitario = 500
        cantidad = 1
 
        # Funcionalidad
        valor_total, impuesto = impuestos_logic.calcular_impuesto(
            categoria,
            precio_unitario,
            cantidad
        )
 
        # Salidas Esperadas
        valor_total_esperado = 500
        impuesto_esperado = 73
 
        # Verificacion
        self.assertEqual(valor_total_esperado, valor_total)
        self.assertEqual(impuesto_esperado, impuesto)
 
 
    # ---------- CASOS DE ERROR ----------
    def test_error_1(self):
        # Entradas
        categoria = impuestos_logic.IVA_19
        precio_unitario = -50000
        cantidad = 1

        # Verificacion
        with self.assertRaises(impuestos_logic.InvalidPriceError):
            impuestos_logic.calcular_impuesto(categoria, precio_unitario, cantidad)
 
    def test_error_2(self):
        # Entradas
        categoria = impuestos_logic.INC_RESTAURANTES
        precio_unitario = "abc"
        cantidad = 1

        # Verificacion
        with self.assertRaises(impuestos_logic.NonNumericPriceError):
            impuestos_logic.calcular_impuesto(categoria, precio_unitario, cantidad)
 
    def test_error_3(self):
        # Entradas
        categoria = impuestos_logic.BOLSAS_PLASTICAS
        precio_unitario = 500
        cantidad = 0

        # Verificacion
        with self.assertRaises(impuestos_logic.ZeroOrNegativeQuantityError):
            impuestos_logic.calcular_impuesto(categoria, precio_unitario, cantidad)
 
    def test_error_4(self):
        # Entradas
        categoria = impuestos_logic.CIGARRILLOS_VAPEADORES
        precio_unitario = 15000
        cantidad = -10

        # Verificacion
        with self.assertRaises(impuestos_logic.NegativeQuantityError):
            impuestos_logic.calcular_impuesto(categoria, precio_unitario, cantidad)

    def test_precio_cero_lanza_error(self):
        with self.assertRaises(impuestos_logic.InvalidPriceError):
            impuestos_logic.calcular_impuesto(
                categoria=impuestos_logic.IVA_19,
                precio_unitario=0,
                cantidad=1,
            )
 
if __name__ == "__main__":
    unittest.main()
