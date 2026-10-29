
import sys
import unittest
from pathlib import Path

RUTA_SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(RUTA_SRC))

from app import app
from controller.guia_controller import GuiaController
from model.guia_impuestos import GUIA


class TestGuia(unittest.TestCase):

    def test_guia_tiene_ocho_categorias(self):
        datos = GuiaController.armar_guia()
        self.assertEqual(len(datos["impuestos"]), 8)

    def test_guia_contiene_todas_las_categorias(self):
        datos = GuiaController.armar_guia()

        categorias = [
            elemento["categoria"].clave
            for elemento in datos["impuestos"]
        ]

        self.assertEqual(set(categorias), set(GUIA.keys()))

    def test_ejemplos_calculan_impuestos_correctamente(self):
        datos = GuiaController.armar_guia()

        for elemento in datos["impuestos"]:
            categoria = elemento["categoria"]
            informacion = elemento["info"]

            impuesto_esperado = categoria.calcular_impuesto(
                informacion["ejemplo_valor"],
                informacion.get("ejemplo_ml", 0)
            )

            self.assertEqual(
                elemento["ejemplo_impuesto"],
                impuesto_esperado
            )

    def test_pagina_guia_carga_correctamente(self):
        cliente = app.test_client()
        respuesta = cliente.get("/guia/")

        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(
            "¿Qué es un impuesto?".encode("utf-8"),
            respuesta.data
        )


if __name__ == "__main__":
    unittest.main()
