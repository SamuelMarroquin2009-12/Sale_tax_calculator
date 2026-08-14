# Calculadora de Impuestos de Compra – Colombia

Aplicación web que calcula el impuesto de una compra según su categoría de producto, aplicando las tarifas de IVA e INC vigentes en Colombia. Desarrollada en **Python**.

## Nombres de los creadores
- Samuel Marroquín
- Isabella Ruiz Velasquez

## Entradas
El usuario ingresa tres datos:

| Campo | Descripción | Ejemplo |
|---|---|---|
| Categoría | La categoría del producto que va a comprar (una de las 8 definidas) | `iva19` |
| Precio unitario (COP) | Precio de una unidad del producto (en cigarrillos/vapeadores es el precio por mililitro) | 50.000 |
| Cantidad | Unidades compradas (en cigarrillos/vapeadores representa mililitros) | 2 |

Las 8 categorías disponibles son: canasta básica/exento, alimentos IVA 5%, bienes generales IVA 19%, restaurantes (INC 8%), licores, bienes suntuarios, bolsas plásticas y cigarrillos/vapeadores.

## Proceso
1. El usuario ingresa la categoría, el precio unitario y la cantidad.
2. Se valida que la categoría exista, y que precio y cantidad sean numéricos y mayores a cero; si no, se lanza una excepción y se detiene la ejecución.
3. Se calcula el valor total: `valor_total = precio_unitario × cantidad`.
4. Se calcula el impuesto según la fórmula de la categoría:

| Categoría | Fórmula del impuesto |
|---|---|
| Canasta básica / Exento | `valor_total × 0` |
| Alimentos IVA 5% | `valor_total × 0.05` |
| Bienes generales IVA 19% | `valor_total × 0.19` |
| Restaurantes (INC 8%) | `valor_total × 0.08` |
| Licores | `valor_total × 0.49` |
| Bienes suntuarios | `valor_total × 0.19` |
| Bolsas plásticas | `cantidad × 73` |
| Cigarrillos / Vapeadores | `(valor_total × 0.30) + (cantidad × 2000)` |

## Salidas
- **Caso exitoso:** valor total de la compra y monto del impuesto calculado, ambos en pesos colombianos (COP).
- **Caso de error:** excepción con mensaje indicando la causa (ej. "El precio unitario no puede ser negativo").

## Casos de prueba
Ver `Casos_de_prueba LPCL.xlsx`: 10 casos (3 normales, 3 extraordinarios, 4 error).
