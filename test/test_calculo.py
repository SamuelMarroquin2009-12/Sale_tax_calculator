# Pruebas del Model (las reglas para calcular el impuesto). No necesitan base de datos.

# Todas las pruebas unitarias importan la biblioteca unittest
import unittest

import sys
sys.path.append("src")

from model.calculo import Calculo, ErrorValorInvalido, ErrorCategoriaDesconocida


class CalculoTest(unittest.TestCase):
    """ Pruebas de la clase Calculo """

    def calcular(self, categoria, valor, mililitros=0):
        """ Para no repetir lo mismo en cada prueba: crea el cálculo y retorna el impuesto """
        calculo = Calculo(categoria=categoria, valor=valor, mililitros=mililitros)
        return calculo.calcular_impuesto()

    # ---------- Casos normales: uno por cada categoría ----------

    def test_normal_canasta(self):
        # Datos de entrada
        valor = 50000
        # Dato de salida esperado: la canasta básica no paga impuesto
        esperado = 0

        resultado = self.calcular("canasta", valor)

        self.assertAlmostEqual(esperado, resultado, 2)

    def test_normal_alimentos_5(self):
        resultado = self.calcular("alimentos5", 100000)
        self.assertAlmostEqual(5000, resultado, 2)

    def test_normal_general_19(self):
        resultado = self.calcular("general19", 100000)
        self.assertAlmostEqual(19000, resultado, 2)

    def test_normal_restaurante(self):
        resultado = self.calcular("restaurante", 100000)
        self.assertAlmostEqual(8000, resultado, 2)

    def test_normal_licores(self):
        resultado = self.calcular("licores", 200000)
        self.assertAlmostEqual(98000, resultado, 2)

    def test_normal_suntuarios(self):
        resultado = self.calcular("suntuarios", 100000)
        self.assertAlmostEqual(19000, resultado, 2)

    def test_normal_bolsas(self):
        # 10 bolsas x $73 cada una
        resultado = self.calcular("bolsas", 10)
        self.assertAlmostEqual(730, resultado, 2)

    def test_normal_cigarrillos(self):
        # (100000 x 0.30) + (10 ml x 2000) = 30000 + 20000
        resultado = self.calcular("cigarrillos", 100000, 10)
        self.assertAlmostEqual(50000, resultado, 2)

    # ---------- Casos extraordinarios ----------

    def test_extraordinario_valor_cero(self):
        resultado = self.calcular("general19", 0)
        self.assertAlmostEqual(0, resultado, 2)

    def test_extraordinario_coma_decimal(self):
        # En Colombia se escribe 2,5 en vez de 2.5
        resultado = self.calcular("restaurante", "2,5")
        self.assertAlmostEqual(0.2, resultado, 2)

    def test_extraordinario_valor_maximo(self):
        # El valor más grande que se permite todavía se tiene que poder calcular
        resultado = self.calcular("licores", 999999999999)
        self.assertAlmostEqual(489999999999.51, resultado, 2)

    def test_extraordinario_cigarrillos_sin_mililitros(self):
        # Sin mililitros solo se cobra el 30% del valor
        resultado = self.calcular("cigarrillos", 100000, 0)
        self.assertAlmostEqual(30000, resultado, 2)

    def test_extraordinario_espacios_en_el_valor(self):
        resultado = self.calcular("general19", "  100000  ")
        self.assertAlmostEqual(19000, resultado, 2)

    # ---------- Casos de error ----------
    # Con assertRaises verificamos que sí se dispare la excepción esperada

    def test_error_valor_texto(self):
        with self.assertRaises(ErrorValorInvalido):
            self.calcular("general19", "abc")

    def test_error_valor_vacio(self):
        with self.assertRaises(ErrorValorInvalido):
            self.calcular("general19", "")

    def test_error_valor_negativo(self):
        with self.assertRaises(ErrorValorInvalido):
            self.calcular("general19", "-5")

    def test_error_valor_demasiado_grande(self):
        with self.assertRaises(ErrorValorInvalido):
            self.calcular("general19", "1e30")

    def test_error_valor_infinito(self):
        with self.assertRaises(ErrorValorInvalido):
            self.calcular("general19", "inf")

    def test_error_valor_nan(self):
        with self.assertRaises(ErrorValorInvalido):
            self.calcular("general19", "nan")

    def test_error_bolsas_con_decimales(self):
        with self.assertRaises(ErrorValorInvalido):
            self.calcular("bolsas", "2.5")

    def test_error_mililitros_texto(self):
        with self.assertRaises(ErrorValorInvalido):
            self.calcular("cigarrillos", 100000, "abc")

    def test_error_mililitros_negativos(self):
        with self.assertRaises(ErrorValorInvalido):
            self.calcular("cigarrillos", 100000, "-3")

    def test_error_categoria_desconocida(self):
        with self.assertRaises(ErrorCategoriaDesconocida):
            self.calcular("zapatos", 100000)

    def test_error_mensaje_dice_cual_fue_el_dato(self):
        # Un buen mensaje de error debe decir qué dato causó el problema
        with self.assertRaises(ErrorValorInvalido) as contexto:
            self.calcular("general19", "abc")

        self.assertIn("abc", str(contexto.exception))


# Este fragmento de código permite ejecutar la prueba individualmente
# Va fijo en todas las pruebas
if __name__ == '__main__':
    unittest.main()
