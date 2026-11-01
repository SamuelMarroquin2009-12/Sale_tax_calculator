from decimal import Decimal


def formatear_cop(valor) -> str:
    """ 19000 -> '$19.000,00' (formato colombiano) """
    texto = f"{Decimal(str(valor)):,.2f}"
    texto = texto.replace(",", "#").replace(".", ",").replace("#", ".")
    return f"${texto}"
