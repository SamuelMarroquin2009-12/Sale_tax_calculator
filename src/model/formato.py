"""Formato de números y registros para mostrar al usuario."""
from decimal import Decimal


def formatear_cop(valor):
    """19000 -> '$19.000,00' (formato colombiano)."""
    texto = f"{Decimal(str(valor)):,.2f}"
    texto = texto.replace(",", "#").replace(".", ",").replace("#", ".")
    return f"${texto}"


def describir_calculo(registro):
    """Una línea legible de un Calculo guardado en la base de datos."""
    clave = registro.categoria.clave
    if clave == "bolsas":
        entrada = f"{int(registro.valor)} bolsas"
    else:
        entrada = formatear_cop(registro.valor)
        if clave == "cigarrillos":
            ml = Decimal(str(registro.mililitros)).normalize()
            entrada += f" + {ml:f} ml"
    fecha = str(registro.creado)[:16]
    return (f"#{registro.id}  {registro.categoria.nombre}\n"
            f"{entrada}  ->  impuesto {formatear_cop(registro.impuesto)}  ({fecha})")
