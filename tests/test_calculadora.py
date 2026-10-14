"""Pruebas de la lógica compartida por la consola (sin base de datos)."""
from decimal import Decimal

import pytest

from src.controller import controller
from src.model.formato import formatear_cop


@pytest.mark.parametrize("clave, valor, ml, esperado", [
    ("canasta", "50000", 0, "0.00"),
    ("alimentos5", "20000", 0, "1000.00"),
    ("general19", "100000", 0, "19000.00"),
    ("restaurante", "35000", 0, "2800.00"),
    ("licores", "80000", 0, "39200.00"),
    ("suntuarios", "5000000", 0, "950000.00"),
    ("bolsas", "5", 0, "365.00"),
    ("cigarrillos", "15000", "10", "24500.00"),
    ("general19", "0", 0, "0.00"),
    ("general19", "1000,50", 0, "190.10"),   # coma decimal
])
def test_calcular_normal(clave, valor, ml, esperado):
    assert controller.calcular(clave, valor, ml) == Decimal(esperado)


@pytest.mark.parametrize("clave, valor, ml, mensaje", [
    ("general19", "", 0, "número"),
    ("general19", "abc", 0, "número"),
    ("general19", "-5", 0, "negativo"),
    ("general19", "nan", 0, "válido"),
    ("general19", "inf", 0, "válido"),
    ("general19", None, 0, "número"),
    ("bolsas", "1.5", 0, "entero"),
    ("cigarrillos", "15000", "", "Mililitros"),
    ("cigarrillos", "15000", "-3", "negativo"),
    ("juguetes", "100", 0, "Categoría"),
])
def test_calcular_error(clave, valor, ml, mensaje):
    with pytest.raises(ValueError, match=mensaje):
        controller.calcular(clave, valor, ml)


def test_categorias_y_etiquetas():
    assert len(controller.listar_categorias()) == 8
    assert controller.pide_mililitros("cigarrillos")
    assert not controller.pide_mililitros("licores")
    assert "bolsas" in controller.etiqueta_valor("bolsas")


def test_formato_colombiano():
    assert formatear_cop(Decimal("19000")) == "$19.000,00"
    assert formatear_cop("1234567.5") == "$1.234.567,50"
    assert formatear_cop(0) == "$0,00"
