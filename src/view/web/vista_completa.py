"""
Pertenece a la capa de Vista (View), la parte web

Esta es la página web "completa" (la visual, con colores, iconos y modo oscuro).
Hace lo mismo que la versión simple (vista_calculos.py) y usa el mismo Model y el mismo Controller,
solo cambia cómo se ve. Todas sus páginas cuelgan de /completa/
"""
import os

from flask import Blueprint, flash, redirect, render_template, request, url_for

import sys
sys.path.append("src")
from model.calculo import Calculo, CATEGORIAS, CATEGORIA_BOLSAS, CATEGORIA_CIGARRILLOS
from model.calculo import ErrorValorInvalido, ErrorCategoriaDesconocida
from model.formato import formatear_cop
from view.web.guia_impuestos import CONCEPTOS_CLAVE, GUIA, NOMBRES
import controller.calculos_controller as calculos_controller
import controller.tablas_controller as tablas_controller

# Blueprint de la página completa. En app.py se registra con url_prefix="/completa"
blueprint = Blueprint("completa", __name__)

PALABRA_CONFIRMACION = "SI"

MENSAJE_BASE_DE_DATOS = (
    "Hubo un problema con la base de datos. Revise los datos de conexión y que ya haya "
    "creado las tablas. Detalle: "
)


# Filtros: son funciones que las plantillas usan con el símbolo |  (por ejemplo {{ valor|cop }})
@blueprint.app_template_filter("cop")
def filtro_cop(valor):
    return formatear_cop(valor)


@blueprint.app_template_filter("nombre_categoria")
def filtro_nombre_categoria(clave):
    return NOMBRES[clave]


# ---------- Funciones de apoyo ----------

def armar_categorias() -> list:
    """ Lista con los datos de cada tipo de producto que necesita el formulario """
    lista = []
    for clave in CATEGORIAS:
        lista.append({
            "clave": clave,
            "nombre": NOMBRES[clave],
            "pide_ml": clave == CATEGORIA_CIGARRILLOS,
            "etiqueta": "Cantidad de bolsas (unidades)" if clave == CATEGORIA_BOLSAS else "Valor de la compra (COP)"
        })
    return lista


def calcular_ejemplo(clave: str) -> float:
    """ Calcula el impuesto del ejemplo de la guía, usando el Model como cualquier otro cálculo """
    info = GUIA[clave]
    calculo = Calculo(categoria=clave, valor=info["ejemplo_valor"], mililitros=info.get("ejemplo_ml", 0))
    return calculo.calcular_impuesto()


def armar_guia() -> list:
    """ Lista con cada impuesto, su explicación y el impuesto de su ejemplo """
    lista = []
    for categoria in armar_categorias():
        clave = categoria["clave"]
        lista.append({
            "categoria": categoria,
            "info": GUIA[clave],
            "ejemplo_impuesto": calcular_ejemplo(clave)
        })
    return lista


def es_produccion() -> bool:
    """ La aplicación publicada tiene la variable de entorno APP_ENV=production """
    return os.environ.get("APP_ENV", "").lower() == "production"


# ---------- Páginas ----------

@blueprint.route("/")
def inicio():
    """ Página de inicio de la versión completa """
    ejemplo = Calculo(categoria="general19", valor=100000)
    ejemplo.calcular_impuesto()

    return render_template(
        "completa/inicio.html",
        ejemplo_valor=ejemplo.valor,
        ejemplo_tarifa=GUIA["general19"]["tarifa"],
        ejemplo_impuesto=ejemplo.impuesto,
        ejemplo_total=ejemplo.valor + ejemplo.impuesto
    )


@blueprint.route("/guia")
def guia():
    """ Explica en palabras sencillas qué es cada impuesto """
    return render_template("completa/guia.html", impuestos=armar_guia(), conceptos=CONCEPTOS_CLAVE)


@blueprint.route("/calcular", methods=["GET", "POST"])
def calcular():
    """ GET muestra el formulario. POST calcula el impuesto, lo guarda y muestra el resultado """
    datos = {
        "opciones": armar_guia(),
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
        # request.form tiene lo que escribió el usuario (viene por POST, no por la URL)
        datos["elegida"] = request.form.get("categoria", "")
        datos["valor"] = request.form.get("valor", "")
        datos["mililitros"] = request.form.get("mililitros", "")

        calculo = Calculo(
            categoria=datos["elegida"],
            valor=datos["valor"],
            # Si dejaron los mililitros vacíos usamos 0
            mililitros=datos["mililitros"] or "0"
        )

        try:
            calculo.calcular_impuesto()

            # Si la base de datos está en blanco creamos la tabla antes de guardar
            if not tablas_controller.existe_tabla():
                calculos_controller.crear_tabla()
                datos["tabla_creada"] = True

            calculos_controller.insertar(calculo)

            datos["calculo"] = calculo
            datos["categoria"] = {"nombre": NOMBRES[calculo.categoria]}
            datos["tarifa"] = GUIA[calculo.categoria]["tarifa"]
            # Las bolsas pagan un valor fijo por unidad, por eso no tienen "total con impuesto"
            if calculo.categoria != CATEGORIA_BOLSAS:
                datos["total"] = calculo.valor + calculo.impuesto
        except (ErrorValorInvalido, ErrorCategoriaDesconocida) as error:
            datos["error"] = str(error)
        except Exception as error:
            datos["error"] = MENSAJE_BASE_DE_DATOS + str(error)

    return render_template("completa/insertar.html", **datos)


@blueprint.route("/tablas", methods=["GET", "POST"])
def tablas():
    """ Crear o borrar la tabla calculos. Con POST hace la acción y vuelve a mostrar la página """
    if request.method == "POST":
        accion = request.form.get("accion", "")

        try:
            if accion == "crear":
                calculos_controller.crear_tabla()
                flash("La tabla se creó correctamente.", "success")
            elif accion == "borrar":
                if es_produccion():
                    flash("Borrar la tabla está deshabilitado en la aplicación publicada para proteger los datos guardados.", "error")
                elif request.form.get("confirmacion", "") != PALABRA_CONFIRMACION:
                    flash(f"Para eliminar la tabla, escribe {PALABRA_CONFIRMACION}.", "error")
                else:
                    tablas_controller.borrar_tabla()
                    flash("La tabla se eliminó correctamente.", "success")
            else:
                flash("La acción seleccionada no es válida.", "error")
        except Exception as error:
            flash(MENSAJE_BASE_DE_DATOS + str(error), "error")

        # redirect evita que al recargar la página se repita la acción
        return redirect(url_for("completa.tablas"))

    # Estado de la tabla: existe es True, False, o None si no se pudo consultar
    try:
        existe = tablas_controller.existe_tabla()
        estado = {"existe": existe, "total": tablas_controller.contar_calculos() if existe else 0, "mensaje": ""}
    except Exception as error:
        estado = {"existe": None, "total": 0, "mensaje": str(error)}

    return render_template(
        "completa/tablas.html",
        estado=estado,
        palabra=PALABRA_CONFIRMACION,
        borrado_permitido=not es_produccion()
    )


@blueprint.route("/buscar")
def buscar():
    """ Busca por id, por categoría o trae todos, según el parámetro tipo de la URL """
    tipo = request.args.get("tipo", "")
    id_calculo = request.args.get("id_calculo", "")
    categoria = request.args.get("categoria", "")

    resultados = None
    error = None
    total = 0

    if tipo != "":
        try:
            if tipo == "id":
                if id_calculo == "":
                    raise ErrorValorInvalido("Debes ingresar el ID del cálculo.")
                try:
                    resultados = [calculos_controller.buscar_por_id(int(id_calculo))]
                except ValueError:
                    raise ErrorValorInvalido("El ID debe ser un número entero.")
            elif tipo == "categoria":
                if categoria not in CATEGORIAS:
                    raise ErrorCategoriaDesconocida("Debes seleccionar una categoría válida.")
                resultados = calculos_controller.buscar_por_categoria(categoria)
            elif tipo == "todos":
                resultados = calculos_controller.buscar_todos()
            else:
                raise ErrorValorInvalido("El tipo de búsqueda no es válido.")

            # Suma de los impuestos encontrados (round evita decimales raros del float)
            total = round(sum(c.impuesto for c in resultados), 2)
        except (ErrorValorInvalido, ErrorCategoriaDesconocida, calculos_controller.ErrorNoEncontrado) as err:
            resultados = []
            error = str(err)
        except Exception as err:
            resultados = []
            error = MENSAJE_BASE_DE_DATOS + str(err)

    return render_template(
        "completa/buscar.html",
        categorias=armar_categorias(),
        guia=GUIA,
        resultados=resultados,
        error=error,
        total=total,
        id_calculo=id_calculo,
        elegida=categoria
    )
