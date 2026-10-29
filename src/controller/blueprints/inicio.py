from flask import Blueprint, render_template
from model.categoria import Categoria

inicio_bp = Blueprint("inicio", __name__)

VALOR_EJEMPLO = 100000


@inicio_bp.route("/")
def menu_inicio():
    categoria = Categoria.obtener("general19")
    impuesto = categoria.calcular_impuesto(VALOR_EJEMPLO)

    return render_template(
        "inicio.html",
        ejemplo_valor=VALOR_EJEMPLO,
        ejemplo_tarifa="19 %",
        ejemplo_impuesto=impuesto,
        ejemplo_total=VALOR_EJEMPLO + impuesto
    )
