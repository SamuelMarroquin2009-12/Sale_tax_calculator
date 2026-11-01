"""
Pertenece a la capa de Acceso a Datos (Controller)

Funciones extra para administrar la tabla calculos (la usa la página completa):
saber si existe, contar cuántos cálculos tiene y borrarla.
Crear la tabla ya está en calculos_controller.py
"""
import sys
sys.path.append("src")

import controller.calculos_controller as calculos_controller


def existe_tabla() -> bool:
    """ Retorna True si la tabla calculos ya está creada en la base de datos """
    cursor = calculos_controller.obtener_cursor()
    # to_regclass retorna null cuando la tabla no existe
    cursor.execute("select to_regclass('public.calculos') is not null")
    existe = cursor.fetchone()[0]
    cursor.connection.close()

    return existe


def contar_calculos() -> int:
    """ Retorna cuántos cálculos hay guardados. La tabla tiene que existir """
    cursor = calculos_controller.obtener_cursor()
    cursor.execute("select count(*) from calculos")
    total = cursor.fetchone()[0]
    cursor.connection.close()

    return total


def borrar_tabla():
    """
    Borra la tabla calculos completa (DROP) con el script sql/borrar-calculos.sql

    ATENCIÓN: se pierden todos los cálculos guardados
    """
    with open("sql/borrar-calculos.sql", "r") as archivo:
        consulta = archivo.read()

    cursor = calculos_controller.obtener_cursor()
    cursor.execute(consulta)
    cursor.connection.commit()
    cursor.connection.close()
