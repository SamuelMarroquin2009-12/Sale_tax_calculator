# main.py
# Interfaz de consola - Calculadora de Impuestos de Compra - Colombia
# Autores: Samuel Marroquin, Isabella Ruiz Velasquez
import impuestos_logic as ImpuestosLogic
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
    print(f"  {ImpuestosLogic.EXENTO}              -> Canasta básica / Exento")
    print(f"  {ImpuestosLogic.IVA_5}                -> Alimentos con IVA 5%")
    print(f"  {ImpuestosLogic.IVA_19}               -> Bienes generales IVA 19%")
    print(f"  {ImpuestosLogic.INC_RESTAURANTES}     -> Restaurantes (INC 8%)")
    print(f"  {ImpuestosLogic.LICORES}              -> Licores")
    print(f"  {ImpuestosLogic.SUNTUARIOS}           -> Bienes suntuarios")
    print(f"  {ImpuestosLogic.BOLSAS_PLASTICAS}     -> Bolsas plásticas")
    print(f"  {ImpuestosLogic.CIGARRILLOS_VAPEADORES} -> Cigarrillos / Vapeadores")
def main():
    print("=== Calculadora de Impuestos de Compra - Colombia ===")
    print()
    mostrar_categorias()
    print()
    categoria = input("Ingrese la categoría: ").strip()
    precio_unitario = leer_numero("Ingrese el precio unitario (COP): ")
    cantidad = leer_numero("Ingrese la cantidad: ")
    try:
        valor_total, impuesto = ImpuestosLogic.calcular_impuesto(
            categoria, precio_unitario, cantidad
        )
        print()
        print(f"Valor Total:  $ {valor_total:,.2f}")
        print(f"Impuesto:     $ {impuesto:,.2f}")
    except ImpuestosLogic.InvalidCategoryError:
        print("ERROR: La categoría ingresada no es válida")
    except ImpuestosLogic.NonNumericPriceError:
        print("ERROR: El precio unitario debe ser numérico")
    except ImpuestosLogic.NegativePriceError:
        print("ERROR: El precio unitario no puede ser negativo")
    except ImpuestosLogic.NonNumericQuantityError:
        print("ERROR: La cantidad debe ser numérica")
    except ImpuestosLogic.ZeroOrNegativeQuantityError:
        print("ERROR: La cantidad debe ser mayor a 0")
    except ImpuestosLogic.NegativeQuantityError:
        print("ERROR: La cantidad no puede ser negativa") 
if __name__ == "__main__":
    main()
 
