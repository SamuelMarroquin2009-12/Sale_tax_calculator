"""Interfaz de usuario por consola."""
from src.controller import controller
from src.controller.controller import ErrorBaseDatos
from src.model.formato import describir_calculo, formatear_cop

MENU = """
===== Calculadora de impuestos de compra - Colombia =====
1. Crear tablas
2. Borrar tablas
3. Calcular y guardar en la base de datos (INSERT)
4. Buscar cálculos (SELECT)
5. Calcular sin guardar
0. Salir
"""


def _elegir_categoria(permitir_todas=False):
    categorias = controller.listar_categorias()
    for i, (_, nombre, formula) in enumerate(categorias, start=1):
        print(f"  {i}. {nombre}  [{formula}]")
    if permitir_todas:
        print("  0. Todas")
    opcion = input("Categoría: ").strip()
    if permitir_todas and opcion == "0":
        return None
    if not opcion.isdigit() or not 1 <= int(opcion) <= len(categorias):
        raise ValueError("Opción de categoría inválida")
    return categorias[int(opcion) - 1][0]


def _pedir_datos():
    clave = _elegir_categoria()
    valor = input(f"{controller.etiqueta_valor(clave)}: ").strip()
    ml = 0
    if controller.pide_mililitros(clave):
        ml = input("Mililitros de líquido (ml): ").strip()
    return clave, valor, ml


def _insertar():
    registro = controller.insertar_calculo(*_pedir_datos())
    print(f"Guardado (id {registro.id}). "
          f"Impuesto: {formatear_cop(registro.impuesto)} COP")


def _calcular_sin_guardar():
    impuesto = controller.calcular(*_pedir_datos())
    print(f"Impuesto: {formatear_cop(impuesto)} COP")


def _mostrar(registros):
    if not registros:
        print("No se encontraron cálculos.")
        return
    for registro in registros:
        print(describir_calculo(registro))
    total = sum(r.impuesto for r in registros)
    print(f"-- {len(registros)} cálculo(s), impuesto total: {formatear_cop(total)}")


def _buscar():
    print("1. Buscar por categoría   2. Buscar por id")
    modo = input("Opción: ").strip()
    if modo == "1":
        _mostrar(controller.buscar_calculos(_elegir_categoria(True)))
    elif modo == "2":
        id_texto = input("Id: ").strip()
        if not id_texto.isdigit():
            raise ValueError("El id debe ser un número entero")
        _mostrar([controller.buscar_por_id(int(id_texto))])
    else:
        raise ValueError("Opción inválida")


def ejecutar():
    """Bucle del menú. La base de datos ya debe estar conectada."""
    acciones = {
        "1": lambda: (controller.crear_tablas(), print("Tablas creadas.")),
        "2": lambda: (controller.borrar_tablas(), print("Tablas borradas.")),
        "3": _insertar,
        "4": _buscar,
        "5": _calcular_sin_guardar,
    }
    while True:
        print(MENU)
        opcion = input("Opción: ").strip()
        if opcion == "0":
            print("¡Hasta luego!")
            return
        accion = acciones.get(opcion)
        if accion is None:
            print("Opción inválida.")
            continue
        try:
            accion()
        except (ValueError, ErrorBaseDatos) as error:
            print(f"Error: {error}")
