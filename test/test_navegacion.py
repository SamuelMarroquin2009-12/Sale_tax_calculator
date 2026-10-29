
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

RUTA_SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(RUTA_SRC))

from app import app


class TestNavegacion(unittest.TestCase):

    def setUp(self):
        self.cliente = app.test_client()

    def test_tablas_no_disponible_en_produccion(self):
        with patch.dict("os.environ", {"APP_ENV": "production"}):
            respuesta_get = self.cliente.get("/tablas/")

            respuesta_post = self.cliente.post(
                "/tablas/",
                data={
                    "accion": "borrar",
                    "confirmacion": "SI"
                }
            )

        self.assertEqual(respuesta_get.status_code, 404)
        self.assertEqual(respuesta_post.status_code, 404)

    def test_paginas_principales_cargan(self):
        rutas = [
            "/",
            "/guia/",
            "/calculos/nuevo",
            "/tablas/",
            "/calculos/buscar"
        ]

        for ruta in rutas:
            with self.subTest(ruta=ruta):
                if ruta == "/tablas/":
                    with patch(
                        "controller.blueprints.tablas.consultar_estado",
                        return_value={
                            "existe": False,
                            "total": 0,
                            "mensaje": "La tabla no existe."
                        }
                    ):
                        respuesta = self.cliente.get(ruta)
                else:
                    respuesta = self.cliente.get(ruta)

                self.assertEqual(respuesta.status_code, 200)

    def test_menu_resalta_la_pagina_actual(self):
        rutas = [
            ("/", 'href="/"'),
            ("/guia/", 'href="/guia/"'),
            ("/calculos/nuevo", 'href="/calculos/nuevo"'),
            ("/tablas/", 'href="/tablas/"'),
            ("/calculos/buscar", 'href="/calculos/buscar"')
        ]

        for ruta, enlace in rutas:
            with self.subTest(ruta=ruta):
                if ruta == "/tablas/":
                    with patch(
                        "controller.blueprints.tablas.consultar_estado",
                        return_value={
                            "existe": False,
                            "total": 0,
                            "mensaje": "La tabla no existe."
                        }
                    ):
                        respuesta = self.cliente.get(ruta)
                else:
                    respuesta = self.cliente.get(ruta)

                pagina = respuesta.get_data(as_text=True)

                self.assertIn(enlace + ' class="activo" aria-current="page"', pagina)


if __name__ == "__main__":
    unittest.main()
