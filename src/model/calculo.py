"""
Pertenece a la capa de Reglas de Negocio (Model)

Aquí está todo lo que tiene que ver con calcular el impuesto de una compra
y con los errores que pueden pasar si el usuario escribe algo mal.
Este archivo no usa ni la base de datos ni Flask, por eso se puede probar solo.
"""

# Los tipos de producto que se pueden escoger y el nombre que le mostramos al usuario.
# La clave (la de la izquierda) es la que se guarda en la base de datos.
CATEGORIAS = {
    "canasta": "Canasta básica / Exento (0%)",
    "alimentos5": "Alimentos con IVA 5%",
    "general19": "Bienes generales IVA 19%",
    "restaurante": "Restaurantes (INC 8%)",
    "licores": "Licores (49%)",
    "suntuarios": "Bienes suntuarios (19%)",
    "bolsas": "Bolsas plásticas ($73 por bolsa)",
    "cigarrillos": "Cigarrillos / Vapeadores (30% + $2000 por mililitro)",
}

# Las categorías que simplemente cobran un porcentaje del valor de la compra
TARIFAS = {
    "canasta": 0,
    "alimentos5": 0.05,
    "general19": 0.19,
    "restaurante": 0.08,
    "licores": 0.49,
    "suntuarios": 0.19,
}

# Estas dos categorías tienen su propia fórmula. Las dejo como constantes con nombre
# para no tener números sueltos (números mágicos) por el código.
CATEGORIA_BOLSAS = "bolsas"
CATEGORIA_CIGARRILLOS = "cigarrillos"
IMPUESTO_POR_BOLSA = 73
TARIFA_CIGARRILLOS = 0.30
IMPUESTO_POR_MILILITRO = 2000

# El valor más grande que dejamos escribir. Es muchísimo más de lo que cuesta cualquier compra,
# sirve para que si alguien escribe un número gigante salga un mensaje y no un error raro.
VALOR_MAXIMO = 999999999999


class ErrorValorInvalido(Exception):
    """ Se dispara cuando el valor, la cantidad o los mililitros no son un número válido """
    pass


class ErrorCategoriaDesconocida(Exception):
    """ Se dispara cuando el tipo de producto escogido no existe en CATEGORIAS """
    pass


def convertir_a_numero(dato, nombre: str) -> float:
    """
    Convierte lo que escribió el usuario (llega como texto) en un número.
    Dispara ErrorValorInvalido si no es un número entre 0 y VALOR_MAXIMO
    """
    try:
        # En Colombia se escribe 2,5 y Python necesita 2.5, por eso cambio la coma por punto
        numero = float(str(dato).strip().replace(",", "."))
    except ValueError:
        raise ErrorValorInvalido(
            f"El {nombre} '{dato}' no es un número. "
            "Escriba solo dígitos, por ejemplo 50000 (sin puntos de miles)."
        )

    # Esta comparación también rechaza los negativos, "inf" y "nan"
    # (nan no es mayor ni menor que nada, entonces nunca cumple la condición)
    if not (0 <= numero <= VALOR_MAXIMO):
        raise ErrorValorInvalido(
            f"El {nombre} {dato} no es válido. Debe estar entre 0 y {VALOR_MAXIMO}."
        )

    return numero


class Calculo:
    """
    Representa un cálculo de impuesto, es lo mismo que se guarda en la tabla calculos

    Se crea con lo que escribió el usuario y luego se llama a calcular_impuesto()
    """
    def __init__(self, categoria: str, valor, mililitros=0, impuesto=0, id_calculo=None, fecha=None):
        self.id_calculo = id_calculo
        self.categoria = categoria
        self.valor = valor
        self.mililitros = mililitros
        self.impuesto = impuesto
        self.fecha = fecha

    def calcular_impuesto(self) -> float:
        """
        Revisa que los datos estén bien, calcula el impuesto según la categoría y lo deja
        en self.impuesto (redondeado a 2 decimales).

        Dispara ErrorCategoriaDesconocida o ErrorValorInvalido si algo está mal escrito
        """
        if self.categoria not in CATEGORIAS:
            raise ErrorCategoriaDesconocida(
                f"El tipo de producto '{self.categoria}' no existe. Escoja uno de la lista."
            )

        if self.categoria == CATEGORIA_BOLSAS:
            # Aquí el "valor" es la cantidad de bolsas, y las bolsas se cuentan enteras
            self.valor = convertir_a_numero(self.valor, "número de bolsas")
            if self.valor != int(self.valor):
                raise ErrorValorInvalido(
                    f"El número de bolsas {self.valor} no es válido. Escriba un número entero."
                )
            self.mililitros = 0
            impuesto = self.valor * IMPUESTO_POR_BOLSA

        elif self.categoria == CATEGORIA_CIGARRILLOS:
            # Es la única que también necesita los mililitros
            self.valor = convertir_a_numero(self.valor, "valor")
            self.mililitros = convertir_a_numero(self.mililitros, "número de mililitros")
            impuesto = self.valor * TARIFA_CIGARRILLOS + self.mililitros * IMPUESTO_POR_MILILITRO

        else:
            # Todas las demás: un porcentaje del valor
            self.valor = convertir_a_numero(self.valor, "valor")
            self.mililitros = 0
            impuesto = self.valor * TARIFAS[self.categoria]

        # Redondeo para que no queden decimales raros por culpa del float (19000.000000000004)
        self.impuesto = round(impuesto, 2)
        return self.impuesto

    def es_igual(self, otro) -> bool:
        """ Compara esta instancia con otra. Si algo es diferente el assert dispara un error """
        assert self.id_calculo == otro.id_calculo
        assert self.categoria == otro.categoria
        assert self.valor == otro.valor
        assert self.mililitros == otro.mililitros
        assert self.impuesto == otro.impuesto
        return True
