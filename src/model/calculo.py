from decimal import Decimal

from model.categoria import Categoria, a_decimal


class Calculo:
    """
    Pertenece a la Capa de Reglas de Negocio (Model)

    Representa un calculo de impuesto que se almacena en la tabla calculos
    """
    def __init__(self, id_calculo, categoria: str, valor, mililitros, impuesto, fecha=None):
        self.id_calculo = id_calculo
        self.categoria = categoria
        self.valor = valor
        self.mililitros = mililitros
        self.impuesto = impuesto
        self.fecha = fecha

    @staticmethod
    def crear(categoria: str, valor, mililitros=0):
        """
        Valida los datos, calcula el impuesto y retorna un Calculo listo para guardar.
        Dispara una excepcion propia (ErrorValorInvalido o ErrorCategoriaDesconocida) si algun dato es invalido
        """
        cat = Categoria.obtener(categoria)
        valor_decimal = a_decimal(valor, "Cantidad" if categoria == "bolsas" else "Valor")
        ml_decimal = a_decimal(mililitros, "Mililitros") if cat.pide_mililitros() else Decimal("0")
        impuesto = cat.calcular_impuesto(valor_decimal, ml_decimal)
        return Calculo(None, categoria, valor_decimal, ml_decimal, impuesto)

    def is_equal(self, otro) -> bool:
        """ Verifica si esta instancia es igual a otra. Dispara una excepcion si no lo son """
        assert self.id_calculo == otro.id_calculo
        assert self.categoria == otro.categoria
        assert Decimal(self.valor) == Decimal(otro.valor)
        assert Decimal(self.mililitros) == Decimal(otro.mililitros)
        assert Decimal(self.impuesto) == Decimal(otro.impuesto)
        return True
