
import sys
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

RUTA_SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(RUTA_SRC))

from app import app
from model.calculo import Calculo
from model.excepciones import ErrorTablaNoExiste


class TestWeb(unittest.TestCase):

    def setUp(self):
        self.cliente = app.test_client()

    def crear_calculo_prueba(self):
        calculo = Calculo.crear("general19", "100000")
        calculo.id_calculo = 7
        calculo.fecha = datetime.now()
        return calculo

    def test_pagina_calcular_carga(self):
        respuesta = self.cliente.get("/calculos/nuevo")

        self.assertEqual(respuesta.status_code, 200)

    def test_calculo_valido_se_guarda(self):
        with patch(
            "controller.blueprints.calculos.CalculosController.insertar"
        ) as insertar:

            def guardar(calculo):
                calculo.id_calculo = 15
                calculo.fecha = datetime.now()
                return 15

            insertar.side_effect = guardar

            respuesta = self.cliente.post(
                "/calculos/nuevo",
                data={
                    "categoria": "general19",
                    "valor": "100000",
                    "mililitros": "0"
                }
            )

        self.assertEqual(respuesta.status_code, 200)
        insertar.assert_called_once()

    def test_valor_invalido_muestra_error(self):
        with patch(
            "controller.blueprints.calculos.CalculosController.insertar"
        ) as insertar:

            respuesta = self.cliente.post(
                "/calculos/nuevo",
                data={
                    "categoria": "general19",
                    "valor": "abc",
                    "mililitros": "0"
                }
            )

        self.assertEqual(respuesta.status_code, 200)
        insertar.assert_not_called()

    def test_crea_tabla_si_no_existe(self):
        with patch(
            "controller.blueprints.calculos.CalculosController.insertar"
        ) as insertar, patch(
            "controller.blueprints.calculos.CalculosController.crear_tabla"
        ) as crear_tabla:

            insertar.side_effect = [
                ErrorTablaNoExiste("La tabla no existe"),
                16
            ]

            respuesta = self.cliente.post(
                "/calculos/nuevo",
                data={
                    "categoria": "general19",
                    "valor": "100000",
                    "mililitros": "0"
                }
            )

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(insertar.call_count, 2)
        crear_tabla.assert_called_once()

    def test_busqueda_sin_id_muestra_error(self):
        respuesta = self.cliente.get(
            "/calculos/buscar?tipo=id&id_calculo="
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(
            "Debes ingresar el ID del cálculo.",
            respuesta.get_data(as_text=True)
        )

    def test_busqueda_con_id_no_numerico_muestra_error(self):
        respuesta = self.cliente.get(
            "/calculos/buscar?tipo=id&id_calculo=abc"
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(
            "El ID debe ser un número entero.",
            respuesta.get_data(as_text=True)
        )

    def test_busqueda_por_id(self):
        calculo = self.crear_calculo_prueba()

        with patch(
            "controller.blueprints.calculos.CalculosController.buscar_calculo",
            return_value=calculo
        ) as buscar:

            respuesta = self.cliente.get(
                "/calculos/buscar?tipo=id&id_calculo=7"
            )

        self.assertEqual(respuesta.status_code, 200)
        buscar.assert_called_once_with(7)

    def test_busqueda_por_categoria(self):
        calculo = self.crear_calculo_prueba()

        with patch(
            "controller.blueprints.calculos.CalculosController.buscar_por_categoria",
            return_value=[calculo]
        ) as buscar:

            respuesta = self.cliente.get(
                "/calculos/buscar?tipo=categoria&categoria=general19"
            )

        self.assertEqual(respuesta.status_code, 200)
        buscar.assert_called_once_with("general19")

    def test_busqueda_de_todos(self):
        calculo = self.crear_calculo_prueba()

        with patch(
            "controller.blueprints.calculos.CalculosController.buscar_todos",
            return_value=[calculo]
        ) as buscar:

            respuesta = self.cliente.get(
                "/calculos/buscar?tipo=todos"
            )

        self.assertEqual(respuesta.status_code, 200)
        buscar.assert_called_once()


if __name__ == "__main__":
    unittest.main()
