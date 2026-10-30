from decimal import Decimal

from flask import Blueprint, render_template, request

from controller.calculos_controller import CalculosController
from controller.guia_controller import GuiaController
from model.calculo import Calculo
from model.categoria import CLAVE_BOLSAS, Categoria
from model.excepciones import ErrorCalculadora, ErrorTablaNoExiste, ErrorValorInvalido
from model.guia_impuestos import GUIA


calculos_bp = Blueprint("calculos", __name__)

MILILITROS_POR_DEFECTO = "0"

BUSCAR_POR_ID = "id"
BUSCAR_POR_CATEGORIA = "categoria"
BUSCAR_TODOS = "todos"


# ---------- Insertar ----------

def insertar_creando_tabla_si_falta(calculo: Calculo) -> bool:
    """ Guarda el calculo. Si la tabla no existe la crea y reintenta. Retorna True si tuvo que crearla """
    try:
        CalculosController.insertar(calculo)
        return False
    except ErrorTablaNoExiste:
        CalculosController.crear_tabla()
        CalculosController.insertar(calculo)
        return True


def calcular_total(calculo: Calculo) -> Decimal | None:
    """ Las bolsas pagan un valor fijo por unidad, por eso no tienen un total con impuesto """
    if calculo.categoria == CLAVE_BOLSAS:
        return None

    return calculo.valor + calculo.impuesto


def procesar_formulario(formulario) -> dict:
    """ Calcula y guarda lo pedido en el formulario. Retorna los datos que muestra la plantilla """
    categoria_clave = formulario.get("categoria", "")
    datos = {
        "elegida": categoria_clave,
        "valor": formulario.get("valor", ""),
        "mililitros": formulario.get("mililitros", MILILITROS_POR_DEFECTO)
    }

    try:
        calculo = Calculo.crear(
            categoria=categoria_clave,
            valor=datos["valor"],
            mililitros=datos["mililitros"]
        )
        datos["tabla_creada"] = insertar_creando_tabla_si_falta(calculo=calculo)
    except ErrorCalculadora as error:
        datos["error"] = str(error)
        return datos

    datos["calculo"] = calculo
    datos["categoria"] = Categoria.obtener(categoria_clave)
    datos["tarifa"] = GUIA[categoria_clave]["tarifa"]
    datos["total"] = calcular_total(calculo=calculo)
    return datos


@calculos_bp.route("/nuevo", methods=["GET", "POST"])
def insertar_calculo():
    contexto = {
        "opciones": GuiaController.armar_guia()["impuestos"],
        "calculo": None,
        "error": None,
        "tabla_creada": False,
        "categoria": None,
        "tarifa": None,
        "total": None,
        "elegida": "",
        "valor": "",
        "mililitros": ""
    }

    if request.method == "POST":
        contexto.update(procesar_formulario(formulario=request.form))

    return render_template("insertar.html", **contexto)


# ---------- Buscar ----------

def leer_id(texto: str) -> int:
    if not texto:
        raise ErrorValorInvalido("Debes ingresar el ID del cálculo.")

    try:
        return int(texto)
    except ValueError:
        raise ErrorValorInvalido("El ID debe ser un número entero.") from None


def exigir_categoria(clave: str) -> str:
    if not clave:
        raise ErrorValorInvalido("Debes seleccionar una categoría.")

    return clave


def buscar_segun_tipo(tipo: str, id_calculo: str, categoria: str) -> list:
    """ Hace la busqueda pedida. Dispara ErrorValorInvalido si falta un dato o el tipo no existe """
    if tipo == BUSCAR_POR_ID:
        return [CalculosController.buscar_calculo(leer_id(texto=id_calculo))]

    if tipo == BUSCAR_POR_CATEGORIA:
        return CalculosController.buscar_por_categoria(exigir_categoria(clave=categoria))

    if tipo == BUSCAR_TODOS:
        return CalculosController.buscar_todos()

    raise ErrorValorInvalido("El tipo de búsqueda no es válido.")


def ejecutar_busqueda(tipo: str, id_calculo: str, categoria: str) -> tuple:
    """ Retorna (resultados, error). Sin tipo todavia no se pidio ninguna busqueda: (None, None) """
    if not tipo:
        return None, None

    try:
        return buscar_segun_tipo(tipo=tipo, id_calculo=id_calculo, categoria=categoria), None
    except ErrorCalculadora as error:
        return [], str(error)


def sumar_impuestos(resultados: list) -> Decimal:
    return sum((calculo.impuesto for calculo in resultados), Decimal("0.00"))


@calculos_bp.route("/buscar", methods=["GET"])
def buscar_calculos():
    tipo = request.args.get("tipo", "")
    id_calculo = request.args.get("id_calculo", "").strip()
    elegida = request.args.get("categoria", "")

    resultados, error = ejecutar_busqueda(tipo=tipo, id_calculo=id_calculo, categoria=elegida)
    total = None if resultados is None else sumar_impuestos(resultados=resultados)

    return render_template(
        "buscar.html",
        tipo=tipo,
        id_calculo=id_calculo,
        categorias=Categoria.listar(),
        elegida=elegida,
        error=error,
        resultados=resultados,
        total=total,
        guia=GUIA
    )
