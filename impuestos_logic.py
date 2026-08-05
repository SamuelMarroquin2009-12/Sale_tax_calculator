# impuestos_logic.py
# Calculadora de Impuestos de Compra - Colombia
EXENTO = "exento"
IVA_5 = "iva5"
IVA_19 = "iva19"
INC_RESTAURANTES = "inc_restaurantes"
LICORES = "licores"
SUNTUARIOS = "suntuarios"
BOLSAS_PLASTICAS = "bolsas"
CIGARRILLOS_VAPEADORES = "vapeadores"
# Excepciones del proyecto
class NegativePriceError(Exception):
    pass
class NonNumericPriceError(Exception):
    pass
class ZeroOrNegativeQuantityError(Exception):
    pass
class NegativeQuantityError(Exception):
    pass
    
# Funcion principal encargada del calculo de la multiplicacion y extraccion del porcentaje y valor del impuesto
def calcular_impuesto(categoria, precio_unitario, cantidad):
    # Validaciones
    if not isinstance(precio_unitario, (int, float)):
        raise NonNumericPriceError
    if precio_unitario < 0:
        raise NegativePriceError
    if cantidad == 0:
        raise ZeroOrNegativeQuantityError
    if cantidad < 0:
        raise NegativeQuantityError

    valor_total = precio_unitario * cantidad
    if categoria == EXENTO:
        impuesto = 0
    elif categoria == IVA_5:
        impuesto = valor_total * 0.05
    elif categoria == IVA_19:
        impuesto = valor_total * 0.19
    elif categoria == INC_RESTAURANTES:
        impuesto = valor_total * 0.08
    elif categoria == LICORES:
        impuesto = valor_total * 0.49
    elif categoria == SUNTUARIOS:
        impuesto = valor_total * 0.19
    elif categoria == BOLSAS_PLASTICAS:
        impuesto = cantidad * 73
    elif categoria == CIGARRILLOS_VAPEADORES:
        impuesto = (valor_total * 0.30) + (cantidad * 2000)
    else:
        impuesto = 0
    return valor_total, impuesto
