# main.py
# Interfaz de consola (View) - Calculadora de Impuestos de Compra - Colombia
# Autores: Samuel Marroquin, Isabella Ruiz Velasquez

import sys
sys.path.append("src")

# La Vista puede usar al Modelo (regla de acoplamiento del MVC)
from model import impuestos_logic


def leer_numero(mensaje):
    """
    Pide un dato por consola e intenta convertirlo a numero (float).
    Si el usuario escribe texto que no se puede convertir, se devuelve
    el texto tal cual, para que sea calcular_impuesto() quien dispare
    la excepcion correspondiente (asi el programa nunca se cae).
    """
    texto = input(mensaje).strip()
    try:
        return float(texto)
    except ValueError:
        return texto


def mostrar_categorias():
    print("Categorías disponibles:")
    print(f"  {impuestos_logic.EXENTO}              -> Canasta básica / Exento")
    print(f"  {impuestos_logic.IVA_5}                -> Alimentos con IVA 5%")
    print(f"  {impuestos_logic.IVA_19}               -> Bienes generales IVA 19%")
    print(f"  {impuestos_logic.INC_RESTAURANTES}     -> Restaurantes (INC 8%)")
    print(f"  {impuestos_logic.LICORES}              -> Licores")
    print(f"  {impuestos_logic.SUNTUARIOS}           -> Bienes suntuarios")
    print(f"  {impuestos_logic.BOLSAS_PLASTICAS}     -> Bolsas plásticas")
    print(f"  {impuestos_logic.CIGARRILLOS_VAPEADORES} -> Cigarrillos / Vapeadores")


def main():
    print("=== Calculadora de Impuestos de Compra - Colombia ===")
    print()
    mostrar_categorias()
    print()

    categoria = input("Ingrese la categoría: ").strip()
    precio_unitario = leer_numero("Ingrese el precio unitario (COP): ")
    cantidad = leer_numero("Ingrese la cantidad: ")

    try:
        valor_total, impuesto = impuestos_logic.calcular_impuesto(
            categoria, precio_unitario, cantidad
        )
        print()
        print(f"Valor Total:  $ {valor_total:,.2f}")
        print(f"Impuesto:     $ {impuesto:,.2f}")

    except impuestos_logic.InvalidCategoryError:
        print("ERROR: La categoría ingresada no es válida")
    except impuestos_logic.NonNumericPriceError:
        print("ERROR: El precio unitario debe ser numérico")
    except impuestos_logic.NegativePriceError:
        print("ERROR: El precio unitario no puede ser negativo")
    except impuestos_logic.NonNumericQuantityError:
        print("ERROR: La cantidad debe ser numérica")
    except impuestos_logic.ZeroOrNegativeQuantityError:
        print("ERROR: La cantidad debe ser mayor a 0")
    except impuestos_logic.NegativeQuantityError:
        print("ERROR: La cantidad no puede ser negativa")


if __name__ == "__main__":
    main()
