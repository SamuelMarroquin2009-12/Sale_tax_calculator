import os

# Para las aplicaciones web creadas con Flask, siempre se importa la clase Flask
from flask import Flask

import sys
sys.path.append("src")

# Importamos el módulo donde está creado nuestro Blueprint (las páginas de la aplicación)
from view.web import vista_calculos, vista_completa

# Flask constructor: crea la variable que representa nuestra aplicación web
app = Flask(__name__)

# La página completa usa flash() para mostrar avisos, y flash necesita una clave secreta.
# En Render se puede poner la variable SECRET_KEY, en mi computador sirve la de desarrollo.
app.secret_key = os.environ.get("SECRET_KEY", "clave-solo-para-desarrollo-local")

# Registramos los Blueprints para que Flask conozca sus páginas
# 1) La versión simple (la que se presenta), sus páginas están en la raíz: /
app.register_blueprint(vista_calculos.blueprint)
# 2) La versión completa (la visual), todas sus páginas empiezan con /completa
app.register_blueprint(vista_completa.blueprint, url_prefix="/completa")

# Esta línea permite ejecutar la aplicación con: python app.py
if __name__ == '__main__':
    app.run()
