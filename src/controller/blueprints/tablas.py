import os

from flask import Blueprint, flash, redirect, render_template, request, url_for

from controller.calculos_controller import CalculosController
from model.excepciones import ErrorCalculadora


tablas_bp = Blueprint("tablas", __name__)

PALABRA_CONFIRMACION = "SI"
ENTORNO_PRODUCCION = "production"
MENSAJE_BORRADO_BLOQUEADO = (
    "Borrar la tabla está deshabilitado en la aplicación publicada "
    "para proteger los datos guardados."
)


def es_produccion() -> bool:
    """ La aplicacion publicada se identifica con la variable de entorno APP_ENV=production """
    return os.environ.get("APP_ENV", "").lower() == ENTORNO_PRODUCCION


def consultar_estado() -> dict:
    """ Informa si la tabla existe y cuantos calculos tiene. Si la BD falla, lo dice en el mensaje """
    try:
        existe = CalculosController.existe_tabla()
        total = CalculosController.contar_calculos() if existe else 0
    except ErrorCalculadora as error:
        return {"existe": None, "total": 0, "mensaje": str(error)}

    return {"existe": existe, "total": total, "mensaje": ""}


def crear_tabla() -> None:
    CalculosController.crear_tabla()
    flash("La tabla se creó correctamente.", "success")


def borrar_tabla() -> None:
    if es_produccion():
        flash(MENSAJE_BORRADO_BLOQUEADO, "error")
        return

    if request.form.get("confirmacion", "") != PALABRA_CONFIRMACION:
        flash(f"Para eliminar la tabla, escribe {PALABRA_CONFIRMACION}.", "error")
        return

    CalculosController.borrar_tabla()
    flash("La tabla se eliminó correctamente.", "success")


ACCIONES = {
    "crear": crear_tabla,
    "borrar": borrar_tabla
}


def ejecutar_accion(accion: str) -> None:
    """ Ejecuta la accion pedida por el formulario y deja el resultado en un mensaje flash """
    funcion_de_la_accion = ACCIONES.get(accion)

    if funcion_de_la_accion is None:
        flash("La acción seleccionada no es válida.", "error")
        return

    try:
        funcion_de_la_accion()
    except ErrorCalculadora as error:
        flash(str(error), "error")


@tablas_bp.route("/", methods=["GET", "POST"])
def administrar_tablas():
    if request.method == "POST":
        ejecutar_accion(accion=request.form.get("accion", ""))
        return redirect(url_for("tablas.administrar_tablas"))

    return render_template(
        "tablas.html",
        estado=consultar_estado(),
        palabra=PALABRA_CONFIRMACION,
        borrado_permitido=not es_produccion()
    )
