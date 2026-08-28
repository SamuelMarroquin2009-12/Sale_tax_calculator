# Calculadora de Impuestos de Compra – Colombia

Aplicación de consola desarrollada en Python que calcula el impuesto de una compra según su categoría de producto, aplicando las tarifas definidas para el proyecto.

## Nombres de los creadores

- Samuel Marroquín
- Isabella Ruiz Velasquez

## Entradas

El usuario ingresa tres datos:

| Campo | Descripción | Ejemplo |
|---|---|---|
| Categoría | Categoría del producto que desea comprar | `iva19` |
| Precio unitario (COP) | Precio de una unidad del producto | `50000` |
| Cantidad | Cantidad de unidades compradas | `2` |

Las categorías disponibles son:

- Canasta básica / Exento.
- Alimentos IVA 5%.
- Bienes generales IVA 19%.
- Restaurantes INC 8%.
- Licores.
- Bienes suntuarios.
- Bolsas plásticas.
- Cigarrillos / Vapeadores.

## Proceso

1. El usuario ingresa la categoría, el precio unitario y la cantidad.
2. El sistema valida los datos ingresados.
3. El precio unitario y la cantidad deben ser valores numéricos mayores que cero.
4. Se calcula el valor total de la compra.
5. Se calcula el impuesto correspondiente según la categoría.
6. Se muestra el resultado al usuario.

## Salidas

En un caso exitoso, el programa muestra:

- Valor total de la compra.
- Impuesto calculado.

Cuando los datos ingresados no son válidos, el programa lanza una excepción con información sobre el problema y la forma de corregirlo.

## Casos de prueba

Los casos originales del proyecto se encuentran en:

`doc/Casos_de_Prueba_Impuestos.xlsx`

El proyecto cuenta actualmente con 13 pruebas unitarias automatizadas que verifican tanto cálculos válidos como diferentes condiciones de error.

## Arquitectura

El proyecto utiliza una estructura basada en el patrón MVC (Modelo - Vista - Controlador).

### Modelo

Se encuentra en:

`src/model/impuestos_logic.py`

Contiene las reglas de negocio, validaciones, categorías y cálculos relacionados con los impuestos.

### Vista

Se encuentra en:

`src/view/console/main.py`

Es responsable de la interacción mediante consola, incluyendo la entrada de datos y presentación de resultados.

### Controlador

Se encuentra reservado en:

`src/controller/`

Actualmente no contiene lógica adicional porque el proyecto todavía no utiliza persistencia de datos.

## Estructura del proyecto

Sale_tax_calculator/

- doc/
  - Casos_de_Prueba_Impuestos.xlsx
  - Entrevista_Contador.md
  - revision_automatizada.md
  - revisiones_codigo.md
- src/
  - model/
    - __init__.py
    - impuestos_logic.py
  - view/
    - console/
      - main.py
  - controller/
    - __init__.py
- tests/
  - __init__.py
  - test_impuestos.py
- .gitignore
- LICENSE
- README.md

## Reglas de dependencia

- El Modelo no depende de la Vista.
- La Vista utiliza el Modelo para realizar los cálculos.
- La lógica de negocio se mantiene separada de la interfaz de usuario.
- El Controlador queda preparado para futuras funcionalidades.

## Requisitos

- Python 3.10 o superior.

Para comprobar la versión instalada:

`python --version`

El funcionamiento principal del proyecto utiliza únicamente la biblioteca estándar de Python.

Ruff fue utilizado como herramienta de revisión automatizada durante el proceso de calidad del código.

## Cómo ejecutar la interfaz de consola

Desde la raíz del proyecto ejecutar:

`python -m src.view.console.main`

El programa solicitará:

1. Categoría.
2. Precio unitario.
3. Cantidad.

Después mostrará el valor total y el impuesto correspondiente.

## Cómo ejecutar las pruebas unitarias

Desde la raíz del proyecto ejecutar:

`python -m unittest tests.test_impuestos -v`

Actualmente se ejecutan 13 pruebas unitarias.

El resultado esperado al finalizar correctamente es:

`OK`

## Revisión automatizada

Para revisar automáticamente el código se utilizó Ruff.

El comando utilizado fue:

`ruff check .`

Después de realizar las correcciones, el resultado final fue:

`All checks passed!`

La evidencia completa se encuentra en:

`doc/revision_automatizada.md`

## Revisiones de código

La evidencia de la primera y segunda revisión del proyecto se encuentra en:

`doc/revisiones_codigo.md`

Los problemas encontrados durante las revisiones también quedaron registrados mediante Issues de GitHub.