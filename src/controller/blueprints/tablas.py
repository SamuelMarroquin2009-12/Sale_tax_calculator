import os

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from controller.calculos_controller import CalculosController
from model.excepciones import ErrorCalculadora


tablas_bp = Blueprint("tablas", __name__)

PALABRA_CONFIRMACION = "SI"


def consultar_estado() -> dict:
    try:
        resultado = CalculosController._ejecutar(
            "SELECT EXISTS (SELECT FROM information_schema.tables "
            "WHERE table_schema = 'public' AND table_name = 'calculos')",
            traer="uno"
        )

        existe = resultado[0]

        if existe:
            resultado_total = CalculosController._ejecutar(
                "SELECT COUNT(*) FROM calculos",
                traer="uno"
            )
            total = resultado_total[0]
            mensaje = "La tabla de cálculos existe."
        else:
            total = 0
            mensaje = "La tabla de cálculos todavía no existe."

        return {
            "existe": existe,
            "total": total,
            "mensaje": mensaje
        }

    except ErrorCalculadora as error:
        return {
            "existe": None,
            "total": 0,
            "mensaje": str(error)
        }


@tablas_bp.route("/", methods=["GET", "POST"])
def administrar_tablas():
    if os.environ.get("APP_ENV", "").lower() == "production":
        abort(404)

    if request.method == "POST":
        accion = request.form.get("accion", "")

        try:
            if accion == "crear":
                CalculosController.crear_tabla()
                flash("La tabla se creó correctamente.", "success")

            elif accion == "borrar":
                confirmacion = request.form.get("confirmacion", "")

                if confirmacion != PALABRA_CONFIRMACION:
                    flash(
                        f"Para eliminar la tabla, escribe {PALABRA_CONFIRMACION}.",
                        "error"
                    )
                else:
                    CalculosController.borrar_tabla()
                    flash("La tabla se eliminó correctamente.", "success")

            else:
                flash("La acción seleccionada no es válida.", "error")

        except ErrorCalculadora as error:
            flash(str(error), "error")

        return redirect(url_for("tablas.administrar_tablas"))

    estado = consultar_estado()

    return render_template(
        "tablas.html",
        estado=estado,
        palabra=PALABRA_CONFIRMACION
    )
