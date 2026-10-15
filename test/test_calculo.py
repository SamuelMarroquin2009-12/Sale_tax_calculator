# Pruebas del Model Calculo y del Controller contra la base de datos PostgreSQL
# (usan los datos de conexion de secret_config.py)
import unittest
import sys
sys.path.append("src")

from decimal import Decimal
from unittest.mock import patch

from model.calculo import Calculo
from controller.calculos_controller import CalculosController
import secret_config  # el controlador ya dejo la carpeta del proyecto en sys.path


class TestCalculo(unittest.TestCase):

    # ---------- Test Fixtures ----------
    @classmethod
    def setUpClass(cls):
        """ Se ejecuta al inicio de las pruebas solamente: deja la tabla calculos recien creada """
        CalculosController.borrar_tabla()
        CalculosController.crear_tabla()

    def setUp(self):
        """ Se ejecuta antes de cada prueba: la tabla queda sin filas """
        CalculosController.borrar_filas()

    def insertar_y_buscar(self, categoria, valor, mililitros=0):
        calculo = Calculo.crear(categoria, valor, mililitros)
        id_calculo = CalculosController.insertar(calculo)
        buscado = CalculosController.buscar_calculo(id_calculo)
        return calculo, buscado

    # ---------- Crear tabla ----------
    def test_crear_tabla_normal(self):
        CalculosController.crear_tabla()  # crearla otra vez no debe fallar
        self.assertEqual(CalculosController.buscar_todos(), [])

    def test_crear_tabla_error_sin_conexion(self):
        # Con una contrasena incorrecta no se puede conectar: debe dar un mensaje claro
        with patch.object(secret_config, "PGPASSWORD", "contrasena-incorrecta"):
            with self.assertRaisesRegex(Exception, "No se pudo conectar"):
                CalculosController.crear_tabla()

    # ---------- Borrar tabla ----------
    def test_borrar_tabla_normal(self):
        CalculosController.borrar_tabla()
        try:
            # Sin la tabla, buscar debe fallar con un mensaje claro
            with self.assertRaisesRegex(Exception, "no existe"):
                CalculosController.buscar_todos()
        finally:
            CalculosController.crear_tabla()  # dejarla creada para las demas pruebas

    def test_borrar_tabla_error_sin_conexion(self):
        with patch.object(secret_config, "PGPASSWORD", "contrasena-incorrecta"):
            with self.assertRaisesRegex(Exception, "No se pudo conectar"):
                CalculosController.borrar_tabla()

    # ---------- Insertar: casos normales ----------
    def test_insertar_general_19(self):
        calculo, buscado = self.insertar_y_buscar("general19", "100000")
        self.assertTrue(buscado.is_equal(calculo))
        self.assertEqual(buscado.impuesto, Decimal("19000.00"))

    def test_insertar_canasta_exenta(self):
        calculo, buscado = self.insertar_y_buscar("canasta", "50000")
        self.assertTrue(buscado.is_equal(calculo))
        self.assertEqual(buscado.impuesto, Decimal("0.00"))

    def test_insertar_bolsas(self):
        calculo, buscado = self.insertar_y_buscar("bolsas", "5")
        self.assertTrue(buscado.is_equal(calculo))
        self.assertEqual(buscado.impuesto, Decimal("365.00"))

    def test_insertar_cigarrillos_con_mililitros(self):
        calculo, buscado = self.insertar_y_buscar("cigarrillos", "15000", "10")
        self.assertTrue(buscado.is_equal(calculo))
        self.assertEqual(buscado.impuesto, Decimal("24500.00"))
        self.assertEqual(buscado.mililitros, Decimal("10"))

    # ---------- Insertar: casos de error ----------
    def test_insertar_error_valor_negativo(self):
        with self.assertRaisesRegex(ValueError, "negativo"):
            Calculo.crear("restaurante", "-100")
        self.assertEqual(CalculosController.buscar_todos(), [])

    def test_insertar_error_valor_no_numerico(self):
        with self.assertRaisesRegex(ValueError, "número"):
            Calculo.crear("licores", "abc")

    def test_insertar_error_categoria_invalida(self):
        with self.assertRaisesRegex(ValueError, "Categoría"):
            Calculo.crear("juguetes", "1000")

    def test_insertar_error_bolsas_decimales(self):
        with self.assertRaisesRegex(ValueError, "entero"):
            Calculo.crear("bolsas", "2.5")

    def test_insertar_error_rechazado_por_la_base_de_datos(self):
        # La tabla tiene check (valor >= 0): un calculo invalido armado a mano debe ser rechazado
        invalido = Calculo(None, "general19", Decimal("-1"), Decimal("0"), Decimal("-1"))
        with self.assertRaisesRegex(Exception, "Error de base de datos"):
            CalculosController.insertar(invalido)
        self.assertEqual(CalculosController.buscar_todos(), [])

    # ---------- Buscar: casos normales ----------
    def test_buscar_por_id(self):
        calculo, buscado = self.insertar_y_buscar("alimentos5", "20000")
        self.assertEqual(buscado.id_calculo, calculo.id_calculo)
        self.assertEqual(buscado.impuesto, Decimal("1000.00"))

    def test_buscar_por_categoria(self):
        CalculosController.insertar(Calculo.crear("licores", "80000"))
        CalculosController.insertar(Calculo.crear("restaurante", "35000"))
        resultado = CalculosController.buscar_por_categoria("licores")
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].impuesto, Decimal("39200.00"))

    def test_buscar_todos(self):
        CalculosController.insertar(Calculo.crear("licores", "80000"))
        CalculosController.insertar(Calculo.crear("suntuarios", "5000000"))
        self.assertEqual(len(CalculosController.buscar_todos()), 2)

    def test_buscar_categoria_sin_resultados(self):
        self.assertEqual(CalculosController.buscar_por_categoria("bolsas"), [])

    # ---------- Buscar: casos de error ----------
    def test_buscar_error_id_inexistente(self):
        with self.assertRaisesRegex(ValueError, "No existe"):
            CalculosController.buscar_calculo(999999)

    def test_buscar_error_id_no_numerico(self):
        with self.assertRaisesRegex(ValueError, "entero"):
            CalculosController.buscar_calculo("abc")

    def test_buscar_error_categoria_invalida(self):
        with self.assertRaisesRegex(ValueError, "Categoría"):
            CalculosController.buscar_por_categoria("juguetes")


if __name__ == '__main__':
    unittest.main()
