import impuestos_logic as ImpuestosLogic

try:
  
    categoria = input("Ingrese la categoria: ")
    precio_unitario = float(input("Ingrese el precio unitario: "))
    cantidad = int(input("Ingrese la cantidad: "))
    
    valor_total, impuesto = ImpuestosLogic.calcular_impuesto(
        categoria,
        precio_unitario,
        cantidad
    )
    
    print()
    print("Valor Total:", valor_total)
    print("Impuesto:", impuesto)
  
except ImpuestosLogic.NegativePriceError:
    print("ERROR: El precio unitario no puede ser negativo")

except ImpuestosLogic.NonNumericPriceError:
    print("ERROR: El precio unitario debe ser numerico")

except ImpuestosLogic.ZeroOrNegativeQuantityError:
    print("ERROR: La cantidad debe ser mayor a 0")

except ImpuestosLogic.NegativeQuantityError:
    print("ERROR: La cantidad de mililitros no puede ser negativa")
