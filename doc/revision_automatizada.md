# Revisión automatizada de código

## Herramienta utilizada
Para la revisión automatizada del proyecto se utilizó Ruff, una herramienta de análisis estático para código Python.

## Primera revisión
Se ejecutó el siguiente comando:
ruff check .

La herramienta encontró inicialmente 7 problemas en el código.

Posteriormente se ejecutó:
ruff check . --fix

Ruff corrigió automáticamente 6 de los 7 problemas encontrados.

Quedó pendiente el siguiente problema:
UP007 Use X | Y for type annotations

El problema se encontraba en el archivo:
src/model/impuestos_logic.py

Se tenía:
from typing import Union
Numero = Union[int, float]

## Solución realizada
Se eliminó el uso de Union y se utilizó la sintaxis moderna de Python.

El código quedó de la siguiente manera:
Numero = int | float

## Verificación final
Después de realizar las correcciones se ejecutó nuevamente:
ruff check .

El resultado obtenido fue:
All checks passed!

También se ejecutaron nuevamente las pruebas unitarias con:
python -m unittest tests.test_impuestos -v

El resultado fue:
Ran 13 tests
OK

Esto permitió comprobar que las correcciones realizadas no afectaron el funcionamiento del programa.

## Conclusión
La revisión automatizada permitió detectar y corregir problemas relacionados con las convenciones y calidad del código Python.

Ruff encontró inicialmente 7 problemas, corrigió 6 automáticamente y el problema restante fue solucionado manualmente.

Al finalizar la revisión, Ruff no encontró errores pendientes y las 13 pruebas unitarias se ejecutaron correctamente.

