from decimal import Decimal

from flask import Blueprint, render_template, request

from controller.calculos_controller import CalculosController
from controller.guia_controller import GuiaController
from model.calculo import Calculo
from model.categoria import Categoria
from model.excepciones import ErrorCalculadora
from model.guia_impuestos import GUIA


calculos_bp = Blueprint("calculos", __name__)


@calculos_bp.route("/nuevo", methods=["GET", "POST"])
def insertar_calculo():
    opciones = GuiaController.armar_guia()["impuestos"]

    calculo = None
    error = None
    tabla_creada = False
    categoria = None
    tarifa = None
    total = None

    categoria_clave = ""
    valor = ""
    mililitros = ""

    if request.method == "POST":
        categoria_clave = request.form.get("categoria", "")
        valor = request.form.get("valor", "")
        mililitros = request.form.get("mililitros", "0")

        try:
            calculo = Calculo.crear(
                categoria_clave,
                valor,
                mililitros
            )

            try:
                CalculosController.insertar(calculo)
            except Exception as error_insercion:
                from model.excepciones import ErrorTablaNoExiste

                if not isinstance(error_insercion, ErrorTablaNoExiste):
                    raise

                CalculosController.crear_tabla()
                tabla_creada = True
                CalculosController.insertar(calculo)

            categoria = Categoria.obtener(categoria_clave)
            tarifa = GUIA[categoria_clave]["tarifa"]

            if categoria_clave != "bolsas":
                total = calculo.valor + calculo.impuesto

        except ErrorCalculadora as error_calculo:
            error = str(error_calculo)
            calculo = None

    return render_template(
        "insertar.html",
        opciones=opciones,
        calculo=calculo,
        error=error,
        tabla_creada=tabla_creada,
        categoria=categoria,
        tarifa=tarifa,
        total=total,
        elegida=categoria_clave,
        valor=valor,
        mililitros=mililitros
    )


@calculos_bp.route("/buscar", methods=["GET"])
def buscar_calculos():
    tipo = request.args.get("tipo", "")
    id_calculo = request.args.get("id_calculo", "").strip()
    elegida = request.args.get("categoria", "")

    resultados = None
    error = None
    total = None

    try:
        if tipo == "id":
            if not id_calculo:
                error = "Debes ingresar el ID del cálculo."
                resultados = []
            else:
                try:
                    numero_id = int(id_calculo)
                    calculo = CalculosController.buscar_calculo(numero_id)
                    resultados = [calculo]
                except ValueError:
                    error = "El ID debe ser un número entero."
                    resultados = []

        elif tipo == "categoria":
            if not elegida:
                error = "Debes seleccionar una categoría."
                resultados = []
            else:
                resultados = CalculosController.buscar_por_categoria(elegida)

        elif tipo == "todos":
            resultados = CalculosController.buscar_todos()

        elif tipo:
            error = "El tipo de búsqueda no es válido."
            resultados = []

    except ErrorCalculadora as error_busqueda:
        error = str(error_busqueda)
        resultados = []

    if resultados is not None:
        total = sum(
            (calculo.impuesto for calculo in resultados),
            Decimal("0.00")
        )

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
