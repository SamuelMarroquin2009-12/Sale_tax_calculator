import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from model.categoria import Categoria, a_decimal
from model.excepciones import (
    ErrorBaseDeDatos,
    ErrorCalculadora,
    ErrorCategoriaDesconocida,
    ErrorConfiguracion,
    ErrorConexion,
    ErrorNoEncontrado,
    ErrorTablaNoExiste,
    ErrorValorInvalido,
)


class TestJerarquiaExcepciones(unittest.TestCase):

    def test_excepciones_heredan_de_error_calculadora(self):
        self.assertTrue(issubclass(ErrorValorInvalido, ErrorCalculadora))
        self.assertTrue(issubclass(ErrorCategoriaDesconocida, ErrorCalculadora))
        self.assertTrue(issubclass(ErrorNoEncontrado, ErrorCalculadora))
        self.assertTrue(issubclass(ErrorBaseDeDatos, ErrorCalculadora))
        self.assertTrue(issubclass(ErrorConfiguracion, ErrorCalculadora))

    def test_errores_de_base_de_datos(self):
        self.assertTrue(issubclass(ErrorTablaNoExiste, ErrorBaseDeDatos))
        self.assertTrue(issubclass(ErrorConexion, ErrorBaseDeDatos))


class TestErroresDelModelo(unittest.TestCase):

    def test_a_decimal_rechaza_un_valor_invalido(self):
        with self.assertRaises(ErrorValorInvalido):
            a_decimal("abc")

    def test_categoria_desconocida_lanza_excepcion(self):
        with self.assertRaises(ErrorCategoriaDesconocida):
            Categoria.obtener("categoria_que_no_existe")


if __name__ == "__main__":
    unittest.main()