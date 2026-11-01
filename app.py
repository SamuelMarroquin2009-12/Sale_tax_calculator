# Para las aplicaciones web creadas con Flask, siempre se importa la clase Flask
from flask import Flask

import sys
sys.path.append("src")

# Importamos el módulo donde está creado nuestro Blueprint (las páginas de la aplicación)
from view.web import vista_calculos

# Flask constructor: crea la variable que representa nuestra aplicación web
app = Flask(__name__)

# Registramos el Blueprint para que Flask conozca sus páginas
app.register_blueprint(vista_calculos.blueprint)

# Esta línea permite ejecutar la aplicación con: python app.py
if __name__ == '__main__':
    app.run()
