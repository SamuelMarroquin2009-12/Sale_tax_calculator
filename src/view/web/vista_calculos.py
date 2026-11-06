"""
Pertenece a la capa de Vista (View), la parte web

Aquí está el Blueprint con todas las páginas. Cada función recibe lo que escribe el usuario,
le pide el trabajo al Model y al Controller, y muestra el resultado con una plantilla HTML.
"""
from flask import Blueprint, render_template, request

import sys
sys.path.append("src")
from model.calculo import Calculo, CATEGORIAS, ErrorValorInvalido, ErrorCategoriaDesconocida
import controller.calculos_controller as calculos_controller

# Este es el Blueprint, en app.py lo registramos para que Flask conozca estas páginas
blueprint = Blueprint("vista_calculos", __name__)

def mensaje_base_de_datos(error):
    """
    Retorna el mensaje que ve el usuario cuando falla la base de datos.

    El detalle del error (que puede tener el nombre del servidor o del usuario) NO se muestra
    en la página, solo se imprime en la consola donde corre la aplicación (en Render, en Logs).
    """
    print("Error de base de datos:", error)
    return (
        "Hubo un problema con la base de datos. Revise los datos de conexión y que ya haya "
        "creado las tablas desde el menú."
    )


@blueprint.route("/")
def mostrar_inicio():
    """ Menú de inicio: desde aquí se llega a todo lo demás """
    return render_template("index.html")


@blueprint.route("/nuevo")
def mostrar_formulario_nuevo():
    """ Muestra el formulario para escribir los datos de un cálculo nuevo """
    return render_template("nuevo.html", categorias=CATEGORIAS)


@blueprint.route("/guardar")
def guardar_calculo():
    """ Calcula el impuesto con lo que escribió el usuario y lo guarda en la base de datos """
    # request.args es un diccionario con los datos que vienen en la URL
    calculo = Calculo(
        categoria=request.args["categoria"],
        valor=request.args["valor"],
        mililitros=request.args["mililitros"]
    )

    try:
        calculo.calcular_impuesto()
        calculos_controller.insertar(calculo)
        mensaje = f"Listo, el cálculo quedó guardado. El impuesto a pagar es ${calculo.impuesto:.2f}"
        lista = [calculo]
    except (ErrorValorInvalido, ErrorCategoriaDesconocida) as error:
        # Estos son los errores que nosotros mismos definimos, el mensaje ya es claro para el usuario
        mensaje = str(error)
        lista = []
    except Exception as error:
        # Cualquier otro error, casi siempre es la base de datos
        mensaje = mensaje_base_de_datos(error)
        lista = []

    return render_template("resultados.html", mensaje=mensaje, calculos=lista, categorias=CATEGORIAS)


@blueprint.route("/buscar")
def mostrar_formulario_buscar():
    """ Muestra las tres formas de buscar """
    return render_template("buscar.html", categorias=CATEGORIAS)


@blueprint.route("/buscar-id")
def buscar_calculo_por_id():
    """ Busca un solo cálculo por su id """
    # strip() quita los espacios que puedan quedar al copiar y pegar el id
    texto_id = request.args["id"].strip()

    try:
        calculo = calculos_controller.buscar_por_id(texto_id)
        mensaje = "Este es el cálculo que encontramos"
        lista = [calculo]
    except calculos_controller.ErrorNoEncontrado as error:
        mensaje = str(error)
        lista = []
    except Exception as error:
        mensaje = mensaje_base_de_datos(error)
        lista = []

    return render_template("resultados.html", mensaje=mensaje, calculos=lista, categorias=CATEGORIAS)


@blueprint.route("/buscar-categoria")
def buscar_calculos_por_categoria():
    """ Busca todos los cálculos de un tipo de producto """
    categoria = request.args["categoria"]

    try:
        if categoria not in CATEGORIAS:
            raise ErrorCategoriaDesconocida(f"El tipo de producto '{categoria}' no existe. Escoja uno de la lista.")

        lista = calculos_controller.buscar_por_categoria(categoria)
        mensaje = f"Encontramos {len(lista)} cálculo(s) de {CATEGORIAS[categoria]}"
    except ErrorCategoriaDesconocida as error:
        mensaje = str(error)
        lista = []
    except Exception as error:
        mensaje = mensaje_base_de_datos(error)
        lista = []

    return render_template("resultados.html", mensaje=mensaje, calculos=lista, categorias=CATEGORIAS)


@blueprint.route("/buscar-todos")
def buscar_todos_los_calculos():
    """ Muestra todos los cálculos que hay guardados """
    try:
        lista = calculos_controller.buscar_todos()
        mensaje = f"Hay {len(lista)} cálculo(s) guardado(s)"
    except Exception as error:
        mensaje = mensaje_base_de_datos(error)
        lista = []

    return render_template("resultados.html", mensaje=mensaje, calculos=lista, categorias=CATEGORIAS)


@blueprint.route("/crear-tablas")
def crear_tablas():
    """ Crea la tabla calculos en la base de datos. Se puede pulsar varias veces sin problema """
    try:
        calculos_controller.crear_tabla()
        mensaje = "Listo, la tabla calculos está creada"
    except Exception as error:
        mensaje = mensaje_base_de_datos(error)

    return render_template("resultados.html", mensaje=mensaje, calculos=[], categorias=CATEGORIAS)
