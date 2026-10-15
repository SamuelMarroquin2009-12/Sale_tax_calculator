import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from model.categoria import Categoria
from model.calculo import Calculo
from model.formato import formatear_cop
from controller.calculos_controller import CalculosController

try:
    # Mostrar las categorias disponibles
    categorias = Categoria.listar()
    print("Categorías disponibles:")
    for numero, categoria in enumerate(categorias, start=1):
        print(f"  {numero}. {categoria.nombre}   [{categoria.formula}]")

    opcion = input("Elija la categoría (número): ").strip()
    if not opcion.isdigit() or not 1 <= int(opcion) <= len(categorias):
        raise ValueError("Opción de categoría inválida")
    categoria = categorias[int(opcion) - 1]

    # Pedir al usuario los datos para llenar el calculo
    valor = input(f"{categoria.etiqueta_valor()}: ")
    mililitros = input("Mililitros de líquido (ml): ") if categoria.pide_mililitros() else 0

    # Crear la instancia del Modelo (valida y calcula el impuesto)
    calculo = Calculo.crear(categoria.clave, valor, mililitros)

    # Llamar al controlador para que inserte en la BD
    CalculosController.insertar(calculo)

    print(f"Cálculo guardado (id {calculo.id_calculo}). Impuesto: {formatear_cop(calculo.impuesto)} COP")
except Exception as err:
    print("Error:")
    print(str(err))
