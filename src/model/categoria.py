from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from model.excepciones import ErrorCategoriaDesconocida, ErrorValorInvalido


def a_decimal(dato, nombre="Valor"):
    """ Convierte la entrada a Decimal. Dispara ErrorValorInvalido con mensaje claro si no es valida """
    if isinstance(dato, bool) or dato is None:
        raise ErrorValorInvalido(f"{nombre}: debe ser un número")
    try:
        numero = Decimal(str(dato).strip().replace(",", "."))
    except InvalidOperation:
        raise ErrorValorInvalido(f"{nombre}: debe ser un número (ej. 50000)") from None
    if not numero.is_finite():
        raise ErrorValorInvalido(f"{nombre}: debe ser un número válido")
    if numero < 0:
        raise ErrorValorInvalido(f"{nombre}: no puede ser negativo")
    return numero


class Categoria:
    """
    Pertenece a la Capa de Reglas de Negocio (Model)

    Representa una categoria de producto y sabe calcular su impuesto de compra
    """
    def __init__(self, clave: str, nombre: str, formula: str, tarifa: Decimal = Decimal("0")):
        self.clave = clave
        self.nombre = nombre
        self.formula = formula
        self.tarifa = tarifa

    def pide_mililitros(self) -> bool:
        """ Solo cigarrillos / vapeadores necesitan ademas los mililitros de liquido """
        return self.clave == "cigarrillos"

    def etiqueta_valor(self) -> str:
        """ Texto del dato principal que pide la categoria """
        if self.clave == "bolsas":
            return "Cantidad de bolsas (unidades)"
        return "Valor de la compra (COP)"

    def calcular_impuesto(self, valor, mililitros=0) -> Decimal:
        """ Aplica la formula de la categoria. Retorna el impuesto con 2 decimales """
        valor = a_decimal(valor, "Cantidad" if self.clave == "bolsas" else "Valor")

        if self.clave == "bolsas":
            if valor != valor.to_integral_value():
                raise ErrorValorInvalido("Cantidad: debe ser un número entero de bolsas")
            impuesto = valor * Decimal("73")
        elif self.clave == "cigarrillos":
            ml = a_decimal(mililitros, "Mililitros")
            impuesto = valor * Decimal("0.30") + ml * Decimal("2000")
        else:
            impuesto = valor * self.tarifa

        return impuesto.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @staticmethod
    def listar() -> list:
        """ Todas las categorias disponibles """
        return list(CATEGORIAS.values())

    @staticmethod
    def obtener(clave: str):
        """ Busca una categoria por su clave. Dispara ErrorCategoriaDesconocida si no existe """
        if clave not in CATEGORIAS:
            raise ErrorCategoriaDesconocida(f"Categoría desconocida: {clave!r}")
        return CATEGORIAS[clave]


CATEGORIAS = {
    "canasta":     Categoria("canasta", "Canasta básica / Exento", "valor x 0", Decimal("0")),
    "alimentos5":  Categoria("alimentos5", "Alimentos con IVA 5%", "valor x 0.05", Decimal("0.05")),
    "general19":   Categoria("general19", "Bienes generales IVA 19%", "valor x 0.19", Decimal("0.19")),
    "restaurante": Categoria("restaurante", "Restaurantes (INC 8%)", "valor x 0.08", Decimal("0.08")),
    "licores":     Categoria("licores", "Licores", "valor x 0.49", Decimal("0.49")),
    "suntuarios":  Categoria("suntuarios", "Bienes suntuarios", "valor x 0.19", Decimal("0.19")),
    "bolsas":      Categoria("bolsas", "Bolsas plásticas", "cantidad x 73"),
    "cigarrillos": Categoria("cigarrillos", "Cigarrillos / Vapeadores", "(valor x 0.30) + (ml x 2000)"),
}