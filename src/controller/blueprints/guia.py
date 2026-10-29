from flask import Blueprint, render_template

from controller.guia_controller import GuiaController

guia_bp = Blueprint("guia", __name__)


@guia_bp.route("/")
def guia_impuestos():
    return render_template(
        "guia.html",
        **GuiaController.armar_guia()
    )
