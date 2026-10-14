"""Conexión resiliente: debe funcionar en cualquier computador."""
from types import SimpleNamespace

from src.controller import controller
from src.model import database
from src.model.database import db
from src.model.models import Categoria


def test_cargar_config_encuentra_archivo(tmp_path, monkeypatch):
    (tmp_path / "secret_config.py").write_text('DB_NAME = "prueba"\n')
    monkeypatch.chdir(tmp_path)
    assert database.cargar_config().DB_NAME == "prueba"


def test_conectar_sin_config_usa_sqlite_local(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "cargar_config", lambda: None)
    motor, aviso = database.conectar(tmp_path)
    assert motor == database.MOTOR_SQLITE
    assert "secret_config" in aviso
    assert (tmp_path / "calculadora.db").exists()
    database.cerrar()


def test_conectar_con_datos_malos_usa_sqlite_local(tmp_path, monkeypatch):
    config_mala = SimpleNamespace(DB_HOST="127.0.0.1", DB_PORT=1, DB_NAME="x",
                                  DB_USER="x", DB_PASSWORD="x")
    monkeypatch.setattr(database, "cargar_config", lambda: config_mala)
    motor, aviso = database.conectar(tmp_path)
    assert motor == database.MOTOR_SQLITE
    assert "No se pudo conectar" in aviso
    database.cerrar()


def test_iniciar_base_datos_deja_todo_listo(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "cargar_config", lambda: None)
    controller.iniciar_base_datos(tmp_path)
    assert Categoria.select().count() == 8
    controller.insertar_calculo("licores", "1000")
    assert len(controller.buscar_calculos()) == 1
    controller.cerrar_base_datos()
    assert db.is_closed()
