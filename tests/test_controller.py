from decimal import Decimal

import pytest
from peewee import SqliteDatabase

from src.controller import controller
from src.controller.controller import ErrorBaseDatos
from src.model.database import db
from src.model.models import Calculo, Categoria


# ---------- Crear / borrar tablas ----------
def test_crear_tablas_normal(tablas):
    assert Categoria.table_exists() and Calculo.table_exists()
    assert Categoria.select().count() == 8


def test_crear_tablas_dos_veces_no_duplica(tablas):
    controller.crear_tablas()
    assert Categoria.select().count() == 8


def test_borrar_tablas_normal(tablas):
    controller.borrar_tablas()
    assert not Categoria.table_exists() and not Calculo.table_exists()


def test_buscar_sin_tablas_error():
    database = SqliteDatabase(":memory:")
    db.initialize(database)
    with pytest.raises(ErrorBaseDatos, match="tablas"):
        controller.buscar_calculos()
    database.close()


def test_insertar_sin_categorias_error(tablas):
    Calculo.delete().execute()
    Categoria.delete().execute()
    with pytest.raises(ErrorBaseDatos, match="Crear tablas"):
        controller.insertar_calculo("licores", "1000")


# ---------- Insertar: casos normales ----------
def test_insertar_general_19(tablas):
    r = controller.insertar_calculo("general19", "100000")
    assert r.impuesto == Decimal("19000.00")


def test_insertar_canasta_exento(tablas):
    r = controller.insertar_calculo("canasta", "50000")
    assert r.impuesto == Decimal("0.00")


def test_insertar_bolsas(tablas):
    r = controller.insertar_calculo("bolsas", "5")
    assert r.impuesto == Decimal("365.00")


def test_insertar_cigarrillos_con_ml(tablas):
    r = controller.insertar_calculo("cigarrillos", "15000", "10")
    assert r.impuesto == Decimal("24500.00")  # 15000*0.30 + 10*2000


# ---------- Insertar: casos de error ----------
def test_insertar_valor_negativo_error(tablas):
    with pytest.raises(ValueError, match="negativo"):
        controller.insertar_calculo("restaurante", "-100")
    assert Calculo.select().count() == 0


def test_insertar_valor_no_numerico_error(tablas):
    with pytest.raises(ValueError, match="número"):
        controller.insertar_calculo("licores", "abc")


def test_insertar_categoria_invalida_error(tablas):
    with pytest.raises(ValueError, match="Categoría"):
        controller.insertar_calculo("juguetes", "1000")


def test_insertar_bolsas_decimal_error(tablas):
    with pytest.raises(ValueError, match="entero"):
        controller.insertar_calculo("bolsas", "2.5")


def test_insertar_cigarrillos_ml_negativo_error(tablas):
    with pytest.raises(ValueError, match="negativo"):
        controller.insertar_calculo("cigarrillos", "15000", "-1")


# ---------- Buscar: casos normales ----------
def test_buscar_todos(tablas):
    controller.insertar_calculo("licores", "80000")
    controller.insertar_calculo("suntuarios", "5000000")
    assert len(controller.buscar_calculos()) == 2


def test_buscar_por_categoria(tablas):
    controller.insertar_calculo("licores", "80000")
    controller.insertar_calculo("restaurante", "35000")
    resultado = controller.buscar_calculos("licores")
    assert len(resultado) == 1
    assert resultado[0].impuesto == Decimal("39200.00")


def test_buscar_por_id(tablas):
    r = controller.insertar_calculo("alimentos5", "20000")
    assert controller.buscar_por_id(r.id).impuesto == Decimal("1000.00")


def test_buscar_categoria_sin_resultados(tablas):
    assert controller.buscar_calculos("bolsas") == []


# ---------- Buscar: casos de error ----------
def test_buscar_categoria_invalida_error(tablas):
    with pytest.raises(ValueError, match="Categoría"):
        controller.buscar_calculos("juguetes")


def test_buscar_id_inexistente_error(tablas):
    with pytest.raises(ValueError, match="No existe"):
        controller.buscar_por_id(999)
