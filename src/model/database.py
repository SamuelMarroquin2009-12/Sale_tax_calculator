"""Conexión a la base de datos (ORM Peewee).

Intenta conectar a PostgreSQL (Render) con los datos de secret_config.py.
Si el archivo no existe o la conexión falla, usa una base SQLite local para
que la aplicación funcione igual en cualquier computador.
"""
import importlib.util
import sys
from pathlib import Path

from peewee import DatabaseProxy, PostgresqlDatabase, SqliteDatabase

db = DatabaseProxy()

NOMBRE_CONFIG = "secret_config.py"
MOTOR_POSTGRES = "PostgreSQL (Render)"
MOTOR_SQLITE = "SQLite local"


def directorio_datos_local():
    return Path.home() / ".sale_tax_calculator"


def _carpetas_busqueda():
    carpetas = [Path.cwd()]
    if getattr(sys, "frozen", False):  # ejecutable generado con PyInstaller
        carpetas.append(Path(sys.executable).resolve().parent)
    carpetas.append(Path(__file__).resolve().parents[2])
    return carpetas


def cargar_config():
    """Busca secret_config.py y lo carga. Devuelve el módulo o None."""
    for carpeta in _carpetas_busqueda():
        ruta = carpeta / NOMBRE_CONFIG
        if ruta.is_file():
            especificacion = importlib.util.spec_from_file_location(
                "secret_config", ruta)
            modulo = importlib.util.module_from_spec(especificacion)
            especificacion.loader.exec_module(modulo)
            return modulo
    return None


def _conectar_postgres(config):
    database = PostgresqlDatabase(
        config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT,
        sslmode="require",      # Render exige conexión segura
        connect_timeout=8,
    )
    database.connect()          # prueba real de conexión
    return database


def _conectar_sqlite(carpeta=None):
    carpeta = Path(carpeta) if carpeta else directorio_datos_local()
    carpeta.mkdir(parents=True, exist_ok=True)
    database = SqliteDatabase(str(carpeta / "calculadora.db"))
    database.connect()
    return database


def conectar(carpeta_local=None):
    """Conecta y devuelve (motor, aviso). El aviso es '' si todo salió bien."""
    aviso = ""
    try:
        config = cargar_config()
        if config is None:
            aviso = (f"No se encontró {NOMBRE_CONFIG}: se usa la base local. "
                     "Para usar PostgreSQL revisa el README.")
        else:
            db.initialize(_conectar_postgres(config))
            return MOTOR_POSTGRES, ""
    except Exception as error:  # cualquier fallo -> base local
        aviso = ("No se pudo conectar a PostgreSQL "
                 f"({type(error).__name__}): se usa la base local.")
    db.initialize(_conectar_sqlite(carpeta_local))
    return MOTOR_SQLITE, aviso


def cerrar():
    """Cierra la conexión si está abierta."""
    try:
        if not db.is_closed():
            db.close()
    except Exception:
        pass
