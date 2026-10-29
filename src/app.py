import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

sys.path.append(str(RAIZ))
sys.path.append(str(RAIZ / "src"))

from flask import Flask

from controller.blueprints.calculos import calculos_bp
from controller.blueprints.guia import guia_bp
from controller.blueprints.inicio import inicio_bp
from controller.blueprints.tablas import tablas_bp
from model.categoria import Categoria
from model.formato import formatear_cop


def crear_app() -> Flask:
    """Crea la aplicación web y registra sus páginas."""

    app = Flask(
        __name__,
        template_folder="view-web/templates",
        static_folder="view-web/static"
    )

    app.secret_key = os.environ.get(
        "SECRET_KEY",
        "clave-solo-para-desarrollo-local"
    )

    app.register_blueprint(inicio_bp)
    app.register_blueprint(guia_bp, url_prefix="/guia")
    app.register_blueprint(calculos_bp, url_prefix="/calculos")
    app.register_blueprint(tablas_bp, url_prefix="/tablas")

    app.jinja_env.filters["cop"] = formatear_cop
    app.jinja_env.filters["nombre_categoria"] = (
        lambda clave: Categoria.obtener(clave).nombre
    )

    return app


app = crear_app()


if __name__ == "__main__":
    app.run(
        debug=True,
        port=int(os.environ.get("PORT", 5000))
    )
