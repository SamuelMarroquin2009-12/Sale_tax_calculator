"""Test fixtures: base SQLite en memoria con las tablas creadas."""
import pytest
from peewee import SqliteDatabase

from src.controller import controller
from src.model.database import db


@pytest.fixture
def tablas():
    """Crea las tablas antes de cada prueba y las borra al terminar."""
    database = SqliteDatabase(":memory:")
    db.initialize(database)
    database.connect()
    controller.crear_tablas()
    yield
    controller.borrar_tablas()
    database.close()
