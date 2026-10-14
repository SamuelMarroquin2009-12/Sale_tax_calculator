"""Controller: crear/borrar tablas, calcular, insertar y buscar."""
import functools

from peewee import PeeweeException

from src.model import calculadora
from src.model.calculadora import CATEGORIAS, a_decimal, validar_categoria
from src.model.database import cerrar, conectar, db
from src.model.models import Calculo, Categoria

TABLAS = [Categoria, Calculo]


class ErrorBaseDatos(Exception):
    """Error de base de datos con un mensaje apto para el usuario."""


def _traducir_errores_bd(funcion):
    @functools.wraps(funcion)
    def envoltura(*args, **kwargs):
        try:
            return funcion(*args, **kwargs)
        except PeeweeException as error:
            raise ErrorBaseDatos(
                f"Error de base de datos ({type(error).__name__}). Revisa la "
                "conexión y que las tablas estén creadas (opción 1 del menú).") from error
    return envoltura


# ---------- Cálculo (no necesita base de datos) ----------
def listar_categorias():
    """Lista de (clave, nombre, formula)."""
    return [(clave, nombre, formula)
            for clave, (nombre, formula) in CATEGORIAS.items()]


def etiqueta_valor(clave):
    return calculadora.etiqueta_valor(clave)


def pide_mililitros(clave):
    return calculadora.pide_mililitros(clave)


def calcular(clave, valor, mililitros=0):
    """Calcula el impuesto sin guardar nada."""
    return calculadora.calcular_impuesto(clave, valor, mililitros)


# ---------- Base de datos ----------
def iniciar_base_datos(carpeta_local=None):
    """Conecta (PostgreSQL o SQLite) y asegura las tablas. Devuelve (motor, aviso)."""
    motor, aviso = conectar(carpeta_local)
    try:
        crear_tablas()
    except ErrorBaseDatos as error:
        aviso = f"{aviso} {error}".strip()
    return motor, aviso


def cerrar_base_datos():
    cerrar()


@_traducir_errores_bd
def crear_tablas():
    """CREATE TABLE de todas las tablas y carga las categorías."""
    db.create_tables(TABLAS)
    for clave, (nombre, formula) in CATEGORIAS.items():
        Categoria.get_or_create(
            clave=clave, defaults={"nombre": nombre, "formula": formula})


@_traducir_errores_bd
def borrar_tablas():
    """DROP TABLE de todas las tablas (si existen)."""
    db.drop_tables(list(reversed(TABLAS)))


@_traducir_errores_bd
def insertar_calculo(clave, valor, mililitros=0):
    """INSERT INTO calculo: calcula el impuesto y lo guarda. Devuelve el registro."""
    impuesto = calculadora.calcular_impuesto(clave, valor, mililitros)
    categoria = Categoria.get_or_none(Categoria.clave == clave)
    if categoria is None:
        raise ErrorBaseDatos(
            "Las categorías no están cargadas en la base de datos. "
            "Usa la opción 1 del menú (Crear tablas) primero.")
    ml = a_decimal(mililitros, "Mililitros") if clave == "cigarrillos" else 0
    return Calculo.create(categoria=categoria, valor=a_decimal(valor),
                          mililitros=ml, impuesto=impuesto)


@_traducir_errores_bd
def buscar_calculos(clave=None):
    """SELECT: todos los cálculos, o solo los de una categoría."""
    consulta = Calculo.select(Calculo, Categoria).join(Categoria)
    if clave is not None:
        validar_categoria(clave)
        consulta = consulta.where(Categoria.clave == clave)
    return list(consulta.order_by(Calculo.id))


@_traducir_errores_bd
def buscar_por_id(id_calculo):
    """SELECT de un cálculo por su id. Lanza ValueError si no existe."""
    try:
        return (Calculo.select(Calculo, Categoria).join(Categoria)
                .where(Calculo.id == id_calculo).get())
    except Calculo.DoesNotExist:
        raise ValueError(f"No existe un cálculo con id {id_calculo}") from None
