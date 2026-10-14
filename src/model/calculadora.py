"""Lógica de negocio: reglas de impuestos de compra en Colombia."""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

# clave -> (nombre, descripción de la fórmula)
CATEGORIAS = {
    "canasta":     ("Canasta básica / Exento", "valor x 0"),
    "alimentos5":  ("Alimentos con IVA 5%", "valor x 0.05"),
    "general19":   ("Bienes generales IVA 19%", "valor x 0.19"),
    "restaurante": ("Restaurantes (INC 8%)", "valor x 0.08"),
    "licores":     ("Licores", "valor x 0.49"),
    "suntuarios":  ("Bienes suntuarios", "valor x 0.19"),
    "bolsas":      ("Bolsas plásticas", "cantidad x 73"),
    "cigarrillos": ("Cigarrillos / Vapeadores", "(valor x 0.30) + (ml x 2000)"),
}

_TARIFAS = {
    "canasta": Decimal("0"),
    "alimentos5": Decimal("0.05"),
    "general19": Decimal("0.19"),
    "restaurante": Decimal("0.08"),
    "licores": Decimal("0.49"),
    "suntuarios": Decimal("0.19"),
}
_IMPUESTO_BOLSA = Decimal("73")
_TARIFA_CIGARRILLO = Decimal("0.30")
_IMPUESTO_POR_ML = Decimal("2000")


def a_decimal(dato, nombre="Valor"):
    """Convierte la entrada a Decimal o lanza ValueError con mensaje amigable."""
    if isinstance(dato, bool) or dato is None:
        raise ValueError(f"{nombre}: debe ser un número")
    try:
        numero = Decimal(str(dato).strip().replace(",", "."))
    except InvalidOperation:
        raise ValueError(f"{nombre}: debe ser un número (ej. 50000)") from None
    if not numero.is_finite():
        raise ValueError(f"{nombre}: debe ser un número válido")
    if numero < 0:
        raise ValueError(f"{nombre}: no puede ser negativo")
    return numero


def validar_categoria(clave):
    if clave not in CATEGORIAS:
        raise ValueError(f"Categoría desconocida: {clave!r}")


def etiqueta_valor(clave):
    """Texto que describe el dato principal que pide la categoría."""
    validar_categoria(clave)
    if clave == "bolsas":
        return "Cantidad de bolsas (unidades)"
    return "Valor de la compra (COP)"


def pide_mililitros(clave):
    """True si la categoría necesita además los mililitros de líquido."""
    validar_categoria(clave)
    return clave == "cigarrillos"


def calcular_impuesto(clave, valor, mililitros=0):
    """Devuelve el impuesto (Decimal, 2 decimales) de la categoría dada."""
    validar_categoria(clave)
    nombre = "Cantidad" if clave == "bolsas" else "Valor"
    valor = a_decimal(valor, nombre)

    if clave == "bolsas":
        if valor != valor.to_integral_value():
            raise ValueError("Cantidad: debe ser un número entero de bolsas")
        impuesto = valor * _IMPUESTO_BOLSA
    elif clave == "cigarrillos":
        ml = a_decimal(mililitros, "Mililitros")
        impuesto = valor * _TARIFA_CIGARRILLO + ml * _IMPUESTO_POR_ML
    else:
        impuesto = valor * _TARIFAS[clave]

    return impuesto.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
