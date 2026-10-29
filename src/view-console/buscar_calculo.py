import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from model.categoria import Categoria
from model.excepciones import ErrorValorInvalido
from model.formato import formatear_cop
from controller.calculos_controller import CalculosController


def mostrar(calculos):
    if not calculos:
        print("No se encontraron cálculos.")
        return
    for calculo in calculos:
        nombre = Categoria.obtener(calculo.categoria).nombre
        print(f"#{calculo.id_calculo}  {nombre}  |  valor: {formatear_cop(calculo.valor)}"
              f"  |  impuesto: {formatear_cop(calculo.impuesto)}  |  {str(calculo.fecha)[:16]}")
    total = sum(calculo.impuesto for calculo in calculos)
    print(f"-- {len(calculos)} cálculo(s), impuesto total: {formatear_cop(total)}")


try:
    print("Buscar cálculos:")
    print("  1. Por id")
    print("  2. Por categoría")
    print("  3. Todos")
    opcion = input("Opción: ").strip()

    if opcion == "1":
        id_calculo = input("Id del cálculo: ")
        mostrar([CalculosController.buscar_calculo(id_calculo)])
    elif opcion == "2":
        categorias = Categoria.listar()
        for numero, categoria in enumerate(categorias, start=1):
            print(f"  {numero}. {categoria.nombre}")
        eleccion = input("Elija la categoría (número): ").strip()
        if not eleccion.isdigit() or not 1 <= int(eleccion) <= len(categorias):
            raise ErrorValorInvalido("Opción de categoría inválida")
        mostrar(CalculosController.buscar_por_categoria(categorias[int(eleccion) - 1].clave))
    elif opcion == "3":
        mostrar(CalculosController.buscar_todos())
    else:
        raise ErrorValorInvalido("Opción inválida")
except Exception as err:
    print("Error:")
    print(str(err))
