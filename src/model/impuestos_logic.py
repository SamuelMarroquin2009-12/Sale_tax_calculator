"""Lógica de negocio de la calculadora de impuestos."""

Numero = int | float

EXENTO = "exento"
IVA_5 = "iva5"
IVA_19 = "iva19"
INC_RESTAURANTES = "inc_restaurantes"
LICORES = "licores"
SUNTUARIOS = "suntuarios"
BOLSAS_PLASTICAS = "bolsas"
CIGARRILLOS_VAPEADORES = "vapeadores"

CATEGORIAS = {
    EXENTO: "Canasta básica / Exento",
    IVA_5: "Alimentos con IVA 5%",
    IVA_19: "Bienes generales IVA 19%",
    INC_RESTAURANTES: "Restaurantes (INC 8%)",
    LICORES: "Licores",
    SUNTUARIOS: "Bienes suntuarios",
    BOLSAS_PLASTICAS: "Bolsas plásticas",
    CIGARRILLOS_VAPEADORES: "Cigarrillos / Vapeadores",
}

TARIFAS_PORCENTUALES = {
    EXENTO: 0,
    IVA_5: 0.05,
    IVA_19: 0.19,
    INC_RESTAURANTES: 0.08,
    LICORES: 0.49,
    SUNTUARIOS: 0.19,
}

IMPUESTO_FIJO_BOLSA = 73
TARIFA_VAPEADORES_AD_VALOREM = 0.30
IMPUESTO_ESPECIFICO_VAPEADORES_POR_ML = 2000


class InvalidPriceError(Exception):
    """El precio unitario es cero o negativo."""


class NonNumericPriceError(Exception):
    """El precio unitario no es numérico."""


class NonNumericQuantityError(Exception):
    """La cantidad no es numérica."""


class ZeroQuantityError(Exception):
    """La cantidad es igual a cero."""


class NegativeQuantityError(Exception):
    """La cantidad es negativa."""


class InvalidCategoryError(Exception):
    """La categoría ingresada no es válida."""


def validar_categoria(categoria: str) -> None:
    if categoria not in CATEGORIAS:
        raise InvalidCategoryError(
            f"La categoría '{categoria}' no es válida en validar_categoria(). "
            f"Use una de estas categorías: {', '.join(sorted(CATEGORIAS))}."
        )


def validar_precio(precio_unitario: Numero) -> None:
    if isinstance(precio_unitario, bool) or not isinstance(
        precio_unitario, (int, float)
    ):
        raise NonNumericPriceError(
            f"El precio {precio_unitario!r} no es válido en validar_precio() "
            "porque no es numérico. Ingrese un número mayor que cero."
        )

    if precio_unitario <= 0:
        raise InvalidPriceError(
            f"El precio {precio_unitario} no es válido en validar_precio() "
            "porque es cero o negativo. Ingrese un precio mayor que cero."
        )


def validar_cantidad(cantidad: Numero) -> None:
    if isinstance(cantidad, bool) or not isinstance(cantidad, (int, float)):
        raise NonNumericQuantityError(
            f"La cantidad {cantidad!r} no es válida en validar_cantidad() "
            "porque no es numérica. Ingrese una cantidad mayor que cero."
        )

    if cantidad == 0:
        raise ZeroQuantityError(
            "La cantidad 0 no es válida en validar_cantidad(). "
            "Ingrese una cantidad mayor que cero."
        )

    if cantidad < 0:
        raise NegativeQuantityError(
            f"La cantidad {cantidad} no es válida en validar_cantidad() "
            "porque es negativa. Ingrese una cantidad mayor que cero."
        )


def calcular_impuesto_porcentual(
    valor_total: Numero,
    tarifa: float,
) -> Numero:
    return valor_total * tarifa


def calcular_impuesto_bolsas(cantidad: Numero) -> Numero:
    return cantidad * IMPUESTO_FIJO_BOLSA


def calcular_impuesto_vapeadores(
    valor_total: Numero,
    cantidad: Numero,
) -> Numero:
    return (
        valor_total * TARIFA_VAPEADORES_AD_VALOREM
        + cantidad * IMPUESTO_ESPECIFICO_VAPEADORES_POR_ML
    )


def calcular_impuesto_categoria(
    categoria: str,
    valor_total: Numero,
    cantidad: Numero,
) -> Numero:
    if categoria in TARIFAS_PORCENTUALES:
        return calcular_impuesto_porcentual(
            valor_total=valor_total,
            tarifa=TARIFAS_PORCENTUALES[categoria],
        )

    if categoria == BOLSAS_PLASTICAS:
        return calcular_impuesto_bolsas(cantidad=cantidad)

    return calcular_impuesto_vapeadores(
        valor_total=valor_total,
        cantidad=cantidad,
    )


def calcular_impuesto(
    categoria: str,
    precio_unitario: Numero,
    cantidad: Numero,
) -> tuple[Numero, Numero]:
    validar_categoria(categoria=categoria)
    validar_precio(precio_unitario=precio_unitario)
    validar_cantidad(cantidad=cantidad)

    valor_total = precio_unitario * cantidad

    impuesto = calcular_impuesto_categoria(
        categoria=categoria,
        valor_total=valor_total,
        cantidad=cantidad,
    )

    return valor_total, impuesto