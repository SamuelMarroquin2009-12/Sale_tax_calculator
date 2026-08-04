# test_impuestos.py
# Pruebas unitarias - Calculadora de Impuestos de Compra - Colombia
import unittest
import impuestos_logic as ImpuestosLogic
class ImpuestosTest(unittest.TestCase):
    # ---------- CASOS NORMALES ----------
    def test_normal_1(self):
        # Entradas
        categoria = ImpuestosLogic.IVA_19
        precio_unitario = 50000
        cantidad = 2
        # Proceso
        valor_total, impuesto = ImpuestosLogic.calcular_impuesto(categoria, precio_unitario, cantidad)
        # Verificacion
        self.assertEqual(100000, valor_total)
        self.assertEqual(19000, impuesto)
    def test_normal_2(self):
        categoria = ImpuestosLogic.INC_RESTAURANTES
        precio_unitario = 35000
        cantidad = 1
        valor_total, impuesto = ImpuestosLogic.calcular_impuesto(categoria, precio_unitario, cantidad)
        self.assertEqual(35000, valor_total)
        self.assertEqual(2800, impuesto)
    def test_normal_3(self):
        categoria = ImpuestosLogic.BOLSAS_PLASTICAS
        precio_unitario = 500
        cantidad = 7
        valor_total, impuesto = ImpuestosLogic.calcular_impuesto(categoria, precio_unitario, cantidad)
        self.assertEqual(3500, valor_total)
        self.assertEqual(511, impuesto)
    # ---------- CASOS EXTRAORDINARIOS ----------
    def test_extraordinario_1(self):
        categoria = ImpuestosLogic.IVA_5
        precio_unitario = 15499.75
        cantidad = 1
        valor_total, impuesto = ImpuestosLogic.calcular_impuesto(categoria, precio_unitario, cantidad)
        self.assertAlmostEqual(15499.75, valor_total, 2)
        self.assertAlmostEqual(774.9875, impuesto, 2)

##
