# impuestos_logic.py
# Calculadora de Impuestos de Compra - Colombia
# Autores: Samuel Marroquin, Isabella Ruiz Velasquez
#
# Este modulo contiene la funcionalidad principal del proyecto:
# recibe el precio unitario y la cantidad de un producto, y calcula
# el valor total de la compra junto con el impuesto que corresponde
# segun su categoria.
 
# ------------------------------------------------------------------
# Categorias del proyecto (8 en total)
# ------------------------------------------------------------------
EXENTO = "exento"
IVA_5 = "iva5"
IVA_19 = "iva19"
INC_RESTAURANTES = "inc_restaurantes"
LICORES = "licores"
SUNTUARIOS = "suntuarios"
BOLSAS_PLASTICAS = "bolsas"
CIGARRILLOS_VAPEADORES = "vapeadores"
 
# Conjunto con las categorias validas, usado para validar la entrada
CATEGORIAS_VALIDAS = {
    EXENTO,
    IVA_5,
    IVA_19,
    INC_RESTAURANTES,
    LICORES,
    SUNTUARIOS,
    BOLSAS_PLASTICAS,
    CIGARRILLOS_VAPEADORES,
}
 
 
# ------------------------------------------------------------------
# Excepciones del proyecto
# ------------------------------------------------------------------
class NegativePriceError(Exception):
    """El precio unitario ingresado es negativo."""
    pass
 
 
class NonNumericPriceError(Exception):
    """El precio unitario ingresado no es un numero."""
    pass
 
 
class NonNumericQuantityError(Exception):
    """La cantidad ingresada no es un numero."""
    pass
 
 
class ZeroOrNegativeQuantityError(Exception):
    """La cantidad ingresada es igual a cero."""
    pass
 
 
class NegativeQuantityError(Exception):
    """La cantidad ingresada es negativa."""
    pass
 
 
class InvalidCategoryError(Exception):
    """La categoria ingresada no corresponde a ninguna de las 8 definidas."""
    pass
 
 
# ------------------------------------------------------------------
# Funcion principal
# Las validaciones de error siempre se hacen al comienzo de la funcion
# ------------------------------------------------------------------
def calcular_impuesto(categoria, precio_unitario, cantidad):
    """
    Calcula el valor total de una compra y el impuesto que le
    corresponde, segun la categoria del producto.
 
    Parametros:
        categoria (str): una de las 8 categorias definidas arriba
        precio_unitario (int/float): precio de una unidad del producto
                                      (en cigarrillos/vapeadores es el
                                      precio por mililitro)
        cantidad (int/float): cantidad comprada (en cigarrillos/vapeadores
                               representa mililitros)
 
    Retorna:
        tuple (valor_total, impuesto)
 
    Excepciones:
        InvalidCategoryError        si la categoria no existe
        NonNumericPriceError        si el precio no es numerico
        NegativePriceError          si el precio es negativo
        NonNumericQuantityError     si la cantidad no es numerica
        ZeroOrNegativeQuantityError si la cantidad es igual a cero
        NegativeQuantityError       si la cantidad es negativa
    """
    # --- Validacion de la categoria ---
    if categoria not in CATEGORIAS_VALIDAS:
        raise InvalidCategoryError("La categoría ingresada no es válida")
 
    # --- Validacion del precio unitario ---
    if isinstance(precio_unitario, bool) or not isinstance(precio_unitario, (int, float)):
        raise NonNumericPriceError("El precio unitario debe ser numérico")
 
    if precio_unitario < 0:
        raise NegativePriceError("El precio unitario no puede ser negativo")
 
    # --- Validacion de la cantidad ---
    if isinstance(cantidad, bool) or not isinstance(cantidad, (int, float)):
        raise NonNumericQuantityError("La cantidad debe ser numérica")
 
    if cantidad == 0:
        raise ZeroOrNegativeQuantityError("La cantidad debe ser mayor a 0")
 
    if cantidad < 0:
        raise NegativeQuantityError("La cantidad no puede ser negativa")
 
    # --- Calculo del valor total pagado ---
    valor_total = precio_unitario * cantidad
 
    # --- Calculo del impuesto segun la categoria ---
    if categoria == EXENTO:
        impuesto = valor_total * 0
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
        # Impuesto fijo por bolsa, no depende del valor total
        impuesto = cantidad * 73
    elif categoria == CIGARRILLOS_VAPEADORES:
        # Componente ad valorem (30%) + componente especifico por ml ($2000)
        impuesto = (valor_total * 0.30) + (cantidad * 2000)
 
    return valor_total, impuesto
