# Sale_tax_calculator – Colombia

Aplicación que calcula el impuesto de una compra según su categoría de producto, aplicando las tarifas de IVA e INC vigentes en Colombia. Desarrollada en **Python**.

## Nombres de los creadores
- Samuel Marroquín
- Isabella Ruiz Velasquez
## Entradas
| Categoría | Dato de entrada | Ejemplo |
|---|---|---|
| Canasta básica / Exento | Valor de la compra (COP) | 50.000 |
| Alimentos con IVA 5% | Valor de la compra (COP) | 20.000 |
| Bienes generales IVA 19% | Valor de la compra (COP) | 100.000 |
| Restaurantes (INC 8%) | Valor de la compra (COP) | 35.000 |
| Licores | Valor de la compra (COP) | 80.000 |
| Bienes suntuarios | Valor de la compra (COP) | 5.000.000 |
| Bolsas plásticas | Cantidad de bolsas (unidades) | 5 |
| Cigarrillos / Vapeadores | Valor (COP) + Mililitros de líquido (ml) | 15.000, 10 ml |

## Proceso
1. El usuario selecciona una categoría.
2. Ingresa el dato correspondiente (valor, cantidad, o valor + mililitros).
3. Se valida la entrada; si es inválida, se lanza una excepción y se detiene la ejecución.
4. Se aplica la fórmula de la categoría:

| Categoría | Fórmula |
|---|---|
| Canasta básica / Exento | `valor × 0` |
| Alimentos IVA 5% | `valor × 0.05` |
| Bienes generales IVA 19% | `valor × 0.19` |
| Restaurantes (INC 8%) | `valor × 0.08` |
| Licores | `valor × 0.49` |
| Bienes suntuarios | `valor × 0.19` |
| Bolsas plásticas | `cantidad × 73` |
| Cigarrillos / Vapeadores | `(valor × 0.30) + (ml × 2000)` |

## Salidas
- **Caso exitoso:** monto del impuesto calculado, en pesos colombianos (COP).
- **Caso de error:** excepción con mensaje indicando la causa (ej. "El valor no puede ser negativo").

## Casos de prueba
Ver `Casos_de_Prueba LPCL`: 10 casos (3 normales, 3 extraordinarios, 4 error).

## Notas
Tarifas de IVA e INC según la normativa tributaria colombiana vigente; pueden actualizarse.
