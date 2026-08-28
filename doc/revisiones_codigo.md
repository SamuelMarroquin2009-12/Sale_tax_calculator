# Revisiones de código

## Primera revisión de código
La primera revisión del proyecto se realizó mediante Issues de GitHub.

Durante esta revisión se identificaron problemas relacionados principalmente con:
- Estructura del proyecto.
- Archivos de configuración.
- Nombres de archivos.
- Nombres utilizados dentro del código.
- Números mágicos.
- Anotaciones de tipo.
- Documentación del repositorio.

Los problemas reportados fueron revisados por el equipo y se realizaron las correcciones correspondientes cuando aplicaban.

Algunas recomendaciones no fueron implementadas cuando el equipo determinó que podían agregar complejidad innecesaria al proyecto. En estos casos se dejó una justificación dentro del Issue correspondiente.

## Segunda revisión de código
Para la segunda revisión se utilizó como referencia el documento de Clean Code entregado para la práctica.

Durante esta revisión se analizaron aspectos como:

- Nombres significativos.
- Principio DRY.
- Principio KISS.
- Funciones con una sola responsabilidad.
- Uso de type hints.
- Uso de parámetros nombrados.
- Manejo de excepciones.
- Comentarios innecesarios.
- Duplicación de código.
- Consistencia en los valores retornados por las funciones.
- Organización de las pruebas unitarias.
- Separación de responsabilidades entre modelo y vista.

Los problemas encontrados fueron registrados mediante Issues de GitHub.

Posteriormente se realizaron las correcciones necesarias en una rama independiente y se comprobó que el programa continuara funcionando correctamente.

## Revisión automatizada
Además de las revisiones manuales, se realizó una revisión automatizada utilizando Ruff.

La información completa sobre esta revisión se encuentra en:
`doc/revision_automatizada.md`

Ruff encontró inicialmente 7 problemas. Se corrigieron 6 automáticamente y 1 manualmente.

Después de las correcciones, el resultado final fue:
`All checks passed!`

## Pruebas unitarias
Después de aplicar las correcciones se ejecutaron las pruebas mediante:
`python -m unittest tests.test_impuestos -v`

Resultado:
`Ran 13 tests`
`OK`

Esto permitió verificar que las modificaciones realizadas durante las revisiones no afectaran el funcionamiento esperado del programa.

## Flujo de trabajo utilizado
El flujo utilizado durante las revisiones fue:

Revisión → Issue → Corrección → Pruebas → Commit → Pull Request → Integración

De esta manera se mantiene evidencia de los problemas detectados, las soluciones realizadas y los cambios incorporados al proyecto.