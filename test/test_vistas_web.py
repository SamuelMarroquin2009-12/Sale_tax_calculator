# Pruebas de las páginas web (las dos versiones). Usan el cliente de prueba de Flask,
# que hace como si un navegador entrara a cada página, sin abrir el servidor de verdad.
# ATENCIÓN: borran los cálculos de la base de datos que esté en secret_config.py (usar una base de pruebas)

# Todas las pruebas unitarias importan la biblioteca unittest
import unittest

import sys
sys.path.append("src")
sys.path.append(".")

from app import app
import controller.calculos_controller as calculos_controller
import controller.tablas_controller as tablas_controller


class VistasWebTest(unittest.TestCase):
    """ Pruebas de la versión simple (/) y de la versión completa (/completa/) """

    @classmethod
    def setUpClass(cls):
        calculos_controller.crear_tabla()
        cls.cliente = app.test_client()

    def setUp(self):
        calculos_controller.borrar_filas()

    def pedir(self, url):
        """ Entra a una página con GET y retorna el texto de la respuesta """
        respuesta = self.cliente.get(url)
        self.assertEqual(200, respuesta.status_code)
        return respuesta.get_data(as_text=True)

    # ---------- Versión simple ----------

    def test_simple_menu(self):
        self.assertIn("Calcular y guardar", self.pedir("/"))

    def test_simple_guardar_y_buscar(self):
        texto = self.pedir("/guardar?categoria=general19&valor=100000&mililitros=0")
        self.assertIn("19000", texto)

        self.assertEqual(1, len(calculos_controller.buscar_todos()))
        self.assertIn("19000", self.pedir("/buscar-todos"))

    def test_simple_error_valor_texto(self):
        self.assertIn("no es un número", self.pedir("/guardar?categoria=general19&valor=abc&mililitros=0"))

    # ---------- Versión completa ----------

    def test_completa_todas_las_paginas_abren(self):
        for url in ["/completa/", "/completa/guia", "/completa/calcular", "/completa/tablas", "/completa/buscar"]:
            with self.subTest(url=url):
                self.pedir(url)

    def test_completa_calcular_guarda(self):
        respuesta = self.cliente.post(
            "/completa/calcular", data={"categoria": "licores", "valor": "200000", "mililitros": ""}
        )
        texto = respuesta.get_data(as_text=True)

        self.assertEqual(200, respuesta.status_code)
        # 49% de 200000 = 98000, y la página lo muestra en formato colombiano
        self.assertIn("$98.000,00", texto)
        self.assertEqual(1, len(calculos_controller.buscar_todos()))

    def test_completa_calcular_cigarrillos(self):
        respuesta = self.cliente.post(
            "/completa/calcular", data={"categoria": "cigarrillos", "valor": "100000", "mililitros": "10"}
        )
        self.assertIn("$50.000,00", respuesta.get_data(as_text=True))

    def test_completa_calcular_error(self):
        respuesta = self.cliente.post("/completa/calcular", data={"categoria": "general19", "valor": "abc"})

        self.assertIn("no es un número", respuesta.get_data(as_text=True))
        self.assertEqual([], calculos_controller.buscar_todos())

    def test_completa_calcular_crea_la_tabla_si_no_existe(self):
        # Dejamos la base de datos en blanco, sin la tabla
        tablas_controller.borrar_tabla()
        self.assertFalse(tablas_controller.existe_tabla())

        self.cliente.post("/completa/calcular", data={"categoria": "canasta", "valor": "1000"})

        self.assertTrue(tablas_controller.existe_tabla())
        self.assertEqual(1, len(calculos_controller.buscar_todos()))

    def test_completa_buscar_por_id(self):
        self.cliente.post("/completa/calcular", data={"categoria": "general19", "valor": "100000"})
        id_calculo = calculos_controller.buscar_todos()[0].id_calculo

        texto = self.pedir(f"/completa/buscar?tipo=id&id_calculo={id_calculo}")

        self.assertIn("$19.000,00", texto)

    def test_completa_buscar_id_que_no_existe(self):
        self.assertIn("No existe ningún cálculo", self.pedir("/completa/buscar?tipo=id&id_calculo=999999"))

    def test_completa_buscar_id_no_es_numero(self):
        self.assertIn("debe ser un número entero", self.pedir("/completa/buscar?tipo=id&id_calculo=abc"))

    def test_completa_buscar_por_categoria_y_todos(self):
        self.cliente.post("/completa/calcular", data={"categoria": "licores", "valor": "100000"})
        self.cliente.post("/completa/calcular", data={"categoria": "general19", "valor": "100000"})

        self.assertIn("1 cálculo(s)", self.pedir("/completa/buscar?tipo=categoria&categoria=licores"))
        self.assertIn("2 cálculo(s)", self.pedir("/completa/buscar?tipo=todos"))

    def test_completa_tablas_crear(self):
        respuesta = self.cliente.post("/completa/tablas", data={"accion": "crear"}, follow_redirects=True)

        self.assertIn("La tabla se creó correctamente", respuesta.get_data(as_text=True))

    def test_completa_tablas_borrar_pide_confirmacion(self):
        respuesta = self.cliente.post(
            "/completa/tablas", data={"accion": "borrar", "confirmacion": "no"}, follow_redirects=True
        )

        self.assertIn("escribe SI", respuesta.get_data(as_text=True))
        self.assertTrue(tablas_controller.existe_tabla())

    def test_completa_tablas_borrar_y_volver_a_crear(self):
        self.cliente.post("/completa/tablas", data={"accion": "borrar", "confirmacion": "SI"})
        self.assertFalse(tablas_controller.existe_tabla())

        self.cliente.post("/completa/tablas", data={"accion": "crear"})
        self.assertTrue(tablas_controller.existe_tabla())


# Este fragmento de código permite ejecutar la prueba individualmente
# Va fijo en todas las pruebas
if __name__ == '__main__':
    unittest.main()
