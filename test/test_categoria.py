# Pruebas de las reglas de negocio (no necesitan base de datos)
import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from decimal import Decimal

from model.categoria import Categoria
from model.formato import formatear_cop
from model.excepciones import ErrorCategoriaDesconocida, ErrorValorInvalido


class TestCategoria(unittest.TestCase):

    def calcular(self, clave, valor, mililitros=0):
        return Categoria.obtener(clave).calcular_impuesto(valor, mililitros)

    # ---------- Casos normales: una prueba por categoria ----------
    def test_canasta(self):
        self.assertEqual(self.calcular("canasta", "50000"), Decimal("0.00"))

    def test_alimentos_5(self):
        self.assertEqual(self.calcular("alimentos5", "20000"), Decimal("1000.00"))

    def test_general_19(self):
        self.assertEqual(self.calcular("general19", "100000"), Decimal("19000.00"))

    def test_restaurante(self):
        self.assertEqual(self.calcular("restaurante", "35000"), Decimal("2800.00"))

    def test_licores(self):
        self.assertEqual(self.calcular("licores", "80000"), Decimal("39200.00"))

    def test_suntuarios(self):
        self.assertEqual(self.calcular("suntuarios", "5000000"), Decimal("950000.00"))

    def test_bolsas(self):
        self.assertEqual(self.calcular("bolsas", "5"), Decimal("365.00"))

    def test_cigarrillos(self):
        self.assertEqual(self.calcular("cigarrillos", "15000", "10"), Decimal("24500.00"))

    def test_valor_cero(self):
        self.assertEqual(self.calcular("general19", "0"), Decimal("0.00"))

    def test_coma_decimal(self):
        self.assertEqual(self.calcular("general19", "1000,50"), Decimal("190.10"))

    # ---------- Casos de error ----------
    def test_error_valor_vacio(self):
        with self.assertRaisesRegex(ErrorValorInvalido, "número"):
            self.calcular("general19", "")

    def test_error_valor_texto(self):
        with self.assertRaisesRegex(ErrorValorInvalido, "número"):
            self.calcular("general19", "abc")

    def test_error_valor_negativo(self):
        with self.assertRaisesRegex(ErrorValorInvalido, "negativo"):
            self.calcular("general19", "-5")

    def test_error_valor_infinito(self):
        with self.assertRaisesRegex(ErrorValorInvalido, "válido"):
            self.calcular("general19", "inf")

    def test_error_bolsas_decimales(self):
        with self.assertRaisesRegex(ErrorValorInvalido, "entero"):
            self.calcular("bolsas", "1.5")

    def test_error_mililitros_vacios(self):
        with self.assertRaisesRegex(ErrorValorInvalido, "Mililitros"):
            self.calcular("cigarrillos", "15000", "")

    def test_error_mililitros_negativos(self):
        with self.assertRaisesRegex(ErrorValorInvalido, "negativo"):
            self.calcular("cigarrillos", "15000", "-3")

    def test_error_categoria_invalida(self):
        with self.assertRaisesRegex(ErrorCategoriaDesconocida, "Categoría"):
            Categoria.obtener("juguetes")

    # ---------- Formato ----------
    def test_formato_colombiano(self):
        self.assertEqual(formatear_cop(Decimal("19000")), "$19.000,00")
        self.assertEqual(formatear_cop("1234567.5"), "$1.234.567,50")


if __name__ == '__main__':
    unittest.main()
