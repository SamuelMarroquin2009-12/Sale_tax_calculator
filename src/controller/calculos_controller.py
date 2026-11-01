"""
Pertenece a la capa de Acceso a Datos (Controller)

Es el único que habla con la base de datos PostgreSQL:
crea la tabla calculos, guarda cálculos y los busca.
"""
import os
import sys
sys.path.append("src")

import psycopg2

from model.calculo import Calculo


class ErrorNoEncontrado(Exception):
    """ Se dispara cuando una fila que se busca no existe en la base de datos """
    pass


def obtener_cursor():
    """
    Crea la conexión a la base de datos y retorna un cursor para ejecutar instrucciones
    """
    try:
        # En mi computador los datos secretos están en el archivo secret_config.py
        # (ese archivo NO se sube a GitHub, está en el .gitignore)
        import secret_config
        host = secret_config.PGHOST
        base_de_datos = secret_config.PGDATABASE
        usuario = secret_config.PGUSER
        clave = secret_config.PGPASSWORD
        puerto = secret_config.PGPORT
    except ImportError:
        # En Render no existe ese archivo, ahí los datos secretos se guardan como variables de entorno
        host = os.environ["PGHOST"]
        base_de_datos = os.environ["PGDATABASE"]
        usuario = os.environ["PGUSER"]
        clave = os.environ["PGPASSWORD"]
        puerto = os.environ["PGPORT"]

    connection = psycopg2.connect(database=base_de_datos, user=usuario, password=clave, host=host, port=puerto)

    # Todas las instrucciones se ejecutan a través de un cursor
    return connection.cursor()


def crear_tabla():
    """ Crea la tabla calculos con el script sql/crear-calculos.sql. Si ya existe no pasa nada """
    with open("sql/crear-calculos.sql", "r") as archivo:
        consulta = archivo.read()

    cursor = obtener_cursor()
    cursor.execute(consulta)

    # Las instrucciones que cambian la base de datos necesitan commit() para que queden guardadas
    cursor.connection.commit()
    cursor.connection.close()


def borrar_filas():
    """
    Borra todos los cálculos guardados (DELETE), pero deja la tabla.

    ATENCIÓN: solo se usa en las pruebas. Si se llama en la base de datos real se pierde todo
    """
    cursor = obtener_cursor()
    cursor.execute("delete from calculos")
    cursor.connection.commit()
    cursor.connection.close()


def insertar(calculo: Calculo):
    """
    Guarda un Calculo en la tabla. Al terminar le pone el id y la fecha que le dio la base de datos
    """
    cursor = obtener_cursor()

    # Los %s los llena psycopg2 con los valores de la tupla. Así no se pega el texto del usuario
    # directamente en el SQL y nadie puede meter instrucciones raras.
    cursor.execute(
        """insert into calculos (categoria, valor, mililitros, impuesto)
           values (%s, %s, %s, %s)
           returning id_calculo, fecha""",
        (calculo.categoria, calculo.valor, calculo.mililitros, calculo.impuesto)
    )

    # "returning" nos devuelve el id y la fecha que se acaban de crear
    calculo.id_calculo, calculo.fecha = cursor.fetchone()

    cursor.connection.commit()
    cursor.connection.close()


def convertir_fila_en_calculo(fila):
    """ Convierte una fila que viene de la base de datos en un objeto Calculo """
    # La base de datos devuelve los números como Decimal, aquí los pasamos a float
    # para que sean del mismo tipo que usa el Model
    return Calculo(
        id_calculo=fila[0],
        categoria=fila[1],
        valor=float(fila[2]),
        mililitros=float(fila[3]),
        impuesto=float(fila[4]),
        fecha=fila[5]
    )


def buscar_por_id(id_calculo: int):
    """ Trae un cálculo dado su id. Dispara ErrorNoEncontrado si no existe """
    cursor = obtener_cursor()
    cursor.execute(
        "select id_calculo, categoria, valor, mililitros, impuesto, fecha from calculos where id_calculo = %s",
        (id_calculo,)
    )
    fila = cursor.fetchone()
    cursor.connection.close()

    if fila is None:
        raise ErrorNoEncontrado(
            f"No existe ningún cálculo con el id {id_calculo}. Revise el número o use 'Ver todos' para ver los ids que hay."
        )

    return convertir_fila_en_calculo(fila)


def buscar_por_categoria(categoria: str):
    """ Trae todos los cálculos de un tipo de producto. Si no hay ninguno, retorna una lista vacía """
    cursor = obtener_cursor()
    cursor.execute(
        """select id_calculo, categoria, valor, mililitros, impuesto, fecha
           from calculos where categoria = %s order by id_calculo""",
        (categoria,)
    )
    filas = cursor.fetchall()
    cursor.connection.close()

    # Convertimos cada fila en un Calculo y los vamos guardando en una lista
    lista = []
    for fila in filas:
        lista.append(convertir_fila_en_calculo(fila))

    return lista


def buscar_todos():
    """ Trae todos los cálculos guardados """
    cursor = obtener_cursor()
    cursor.execute(
        "select id_calculo, categoria, valor, mililitros, impuesto, fecha from calculos order by id_calculo"
    )
    filas = cursor.fetchall()
    cursor.connection.close()

    # Convertimos cada fila en un Calculo y los vamos guardando en una lista
    lista = []
    for fila in filas:
        lista.append(convertir_fila_en_calculo(fila))

    return lista
