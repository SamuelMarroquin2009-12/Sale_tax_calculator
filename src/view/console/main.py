"""Interfaz de consola de la calculadora de impuestos."""

from src.model import impuestos_logic


def leer_numero(mensaje: str) -> float:
    """Lee un número desde la consola."""

    texto = input(mensaje).strip()

    try:
        return float(texto)
    except ValueError as error:
        raise ValueError(
            f"El valor '{texto}' no es numérico. Ingrese un número válido."
        ) from error


def mostrar_categorias() -> None:
    """Muestra las categorías disponibles."""

    print("Categorías disponibles:")

    for codigo, descripcion in impuestos_logic.CATEGORIAS.items():
        print(f"  {codigo:<20} -> {descripcion}")


def solicitar_datos() -> tuple[str, float, float]:
    """Solicita los datos necesarios para calcular el impuesto."""

    categoria = input("Ingrese la categoría: ").strip()

    precio_unitario = leer_numero(
        mensaje="Ingrese el precio unitario (COP): "
    )

    cantidad = leer_numero(
        mensaje="Ingrese la cantidad: "
    )

    return categoria, precio_unitario, cantidad


def mostrar_resultado(
    valor_total: impuestos_logic.Numero,
    impuesto: impuestos_logic.Numero,
) -> None:
    """Muestra el resultado del cálculo."""

    print()
    print(f"Valor Total: $ {valor_total:,.2f}")
    print(f"Impuesto: $ {impuesto:,.2f}")


def mostrar_error(error: Exception) -> None:
    """Muestra un mensaje de error."""

    print(f"ERROR: {error}")


def ejecutar_calculo() -> None:
    """Solicita los datos y ejecuta el cálculo del impuesto."""

    categoria, precio_unitario, cantidad = solicitar_datos()

    valor_total, impuesto = impuestos_logic.calcular_impuesto(
        categoria=categoria,
        precio_unitario=precio_unitario,
        cantidad=cantidad,
    )

    mostrar_resultado(
        valor_total=valor_total,
        impuesto=impuesto,
    )


def main() -> None:
    """Inicia la aplicación de consola."""

    print("=== Calculadora de Impuestos de Compra - Colombia ===")
    print()

    mostrar_categorias()
    print()

    try:
        ejecutar_calculo()

    except (
        ValueError,
        impuestos_logic.InvalidCategoryError,
        impuestos_logic.NonNumericPriceError,
        impuestos_logic.InvalidPriceError,
        impuestos_logic.NonNumericQuantityError,
        impuestos_logic.ZeroQuantityError,
        impuestos_logic.NegativeQuantityError,
    ) as error:
        mostrar_error(error=error)


if __name__ == "__main__":
    main()