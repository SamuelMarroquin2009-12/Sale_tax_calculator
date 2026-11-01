# Pruebas del Controller: guardar y buscar cálculos en la base de datos PostgreSQL.
# ATENCIÓN: estas pruebas borran todos los cálculos de la base de datos que esté en secret_config.py
# Úselas solo con una base de datos de pruebas, nunca con la de verdad.

# Todas las pruebas unitarias importan la biblioteca unittest
import unittest

import sys
sys.path.append("src")

from model.calculo import Calculo
import controller.calculos_controller as calculos_controller


class CalculosControllerTest(unittest.TestCase):
    """ Pruebas del controlador de cálculos """

    # TEST FIXTURES
    # Código que se ejecuta antes de las pruebas

    @classmethod
    def setUpClass(cls):
        """ Se ejecuta una sola vez, al inicio de todas las pruebas """
        # Asegura que al inicio la tabla esté creada (sirve también con una base de datos en blanco)
        calculos_controller.crear_tabla()

    def setUp(self):
        """ Se ejecuta antes de cada método de prueba """
        # Asegura que cada prueba empiece con la tabla vacía, así ninguna depende de las otras
        calculos_controller.borrar_filas()

    def crear_y_guardar(self, categoria, valor, mililitros=0):
        """ Para no repetir: crea un cálculo, calcula su impuesto y lo guarda """
        calculo = Calculo(categoria=categoria, valor=valor, mililitros=mililitros)
        calculo.calcular_impuesto()
        calculos_controller.insertar(calculo)
        return calculo

    # ---------- Insertar y buscar ----------

    def test_insertar_y_buscar_por_id(self):
        # Creamos y guardamos un cálculo
        calculo = self.crear_y_guardar("general19", 100000)

        # Lo buscamos por el id que le dio la base de datos
        buscado = calculos_controller.buscar_por_id(calculo.id_calculo)

        # Verificamos que haya traído todos los datos bien
        self.assertTrue(calculo.es_igual(buscado))
        self.assertAlmostEqual(19000, buscado.impuesto, 2)

    def test_insertar_pone_id_y_fecha(self):
        calculo = self.crear_y_guardar("licores", 200000)

        self.assertIsNotNone(calculo.id_calculo)
        self.assertIsNotNone(calculo.fecha)

    def test_insertar_cigarrillos_guarda_los_mililitros(self):
        calculo = self.crear_y_guardar("cigarrillos", 100000, 10)

        buscado = calculos_controller.buscar_por_id(calculo.id_calculo)

        self.assertTrue(calculo.es_igual(buscado))
        self.assertAlmostEqual(10, buscado.mililitros, 2)

    def test_insertar_bolsas(self):
        calculo = self.crear_y_guardar("bolsas", 10)

        buscado = calculos_controller.buscar_por_id(calculo.id_calculo)

        self.assertTrue(calculo.es_igual(buscado))
        self.assertAlmostEqual(730, buscado.impuesto, 2)

    def test_dos_calculos_tienen_ids_diferentes(self):
        primero = self.crear_y_guardar("canasta", 1000)
        segundo = self.crear_y_guardar("canasta", 1000)

        self.assertNotEqual(primero.id_calculo, segundo.id_calculo)

    # ---------- Buscar por categoría y buscar todos ----------

    def test_buscar_por_categoria(self):
        self.crear_y_guardar("licores", 100000)
        self.crear_y_guardar("licores", 200000)
        self.crear_y_guardar("general19", 100000)

        encontrados = calculos_controller.buscar_por_categoria("licores")

        # Solo deben venir los 2 de licores, el de general19 no
        self.assertEqual(2, len(encontrados))
        for calculo in encontrados:
            self.assertEqual("licores", calculo.categoria)

    def test_buscar_por_categoria_sin_resultados(self):
        encontrados = calculos_controller.buscar_por_categoria("licores")

        self.assertEqual([], encontrados)

    def test_buscar_todos(self):
        self.crear_y_guardar("licores", 100000)
        self.crear_y_guardar("general19", 100000)
        self.crear_y_guardar("bolsas", 5)

        encontrados = calculos_controller.buscar_todos()

        self.assertEqual(3, len(encontrados))

    def test_buscar_todos_con_la_tabla_vacia(self):
        self.assertEqual([], calculos_controller.buscar_todos())

    # ---------- Casos de error ----------

    def test_error_buscar_id_que_no_existe(self):
        with self.assertRaises(calculos_controller.ErrorNoEncontrado):
            calculos_controller.buscar_por_id(999999)

    # ---------- Crear la tabla ----------

    def test_crear_tabla_dos_veces_no_falla(self):
        # La tabla ya existe porque setUpClass la creó, crearla otra vez no debe dar error ni borrar datos
        calculo = self.crear_y_guardar("canasta", 1000)

        calculos_controller.crear_tabla()

        self.assertEqual(1, len(calculos_controller.buscar_todos()))
        self.assertTrue(calculo.es_igual(calculos_controller.buscar_por_id(calculo.id_calculo)))


# Este fragmento de código permite ejecutar la prueba individualmente
# Va fijo en todas las pruebas
if __name__ == '__main__':
    unittest.main()
