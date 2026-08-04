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
    pass
