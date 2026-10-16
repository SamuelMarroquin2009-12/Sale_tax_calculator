# Casos de prueba

Pruebas unitarias con `unittest` (39 en total). Ejecución:

```bash
python -m unittest discover -s test -p "*test*.py" -v
```

## test/test_calculo.py – base de datos (20 pruebas)

| Funcionalidad | Tipo | Prueba | Resultado esperado |
|---|---|---|---|
| Crear tabla | Normal | `test_crear_tabla_normal` | Se puede crear (también dos veces) y queda vacía |
| Crear tabla | Error | `test_crear_tabla_error_sin_conexion` | Con contraseña incorrecta: "No se pudo conectar a la base de datos" |
| Borrar tabla | Normal | `test_borrar_tabla_normal` | La tabla se borra; buscar sin tabla da "La tabla 'calculos' no existe" |
| Borrar tabla | Error | `test_borrar_tabla_error_sin_conexion` | Con contraseña incorrecta: "No se pudo conectar a la base de datos" |
| Insertar | Normal | `test_insertar_general_19` | impuesto 19000.00 |
| Insertar | Normal | `test_insertar_canasta_exenta` | impuesto 0.00 |
| Insertar | Normal | `test_insertar_bolsas` | impuesto 365.00 |
| Insertar | Normal | `test_insertar_cigarrillos_con_mililitros` | impuesto 24500.00 |
| Insertar | Error | `test_insertar_error_valor_negativo` | Excepción "negativo"; no se guarda nada |
| Insertar | Error | `test_insertar_error_valor_no_numerico` | Excepción "número" |
| Insertar | Error | `test_insertar_error_categoria_invalida` | Excepción "Categoría" |
| Insertar | Error | `test_insertar_error_bolsas_decimales` | Excepción "entero" |
| Insertar | Error | `test_insertar_error_rechazado_por_la_base_de_datos` | La BD rechaza el valor negativo (check) |
| Buscar | Normal | `test_buscar_por_id` | Trae el cálculo con su impuesto |
| Buscar | Normal | `test_buscar_por_categoria` | 1 resultado, impuesto 39200.00 |
| Buscar | Normal | `test_buscar_todos` | Trae los 2 guardados |
| Buscar | Normal | `test_buscar_categoria_sin_resultados` | Lista vacía |
| Buscar | Error | `test_buscar_error_id_inexistente` | `ErrorNoEncontrado`: "No existe un cálculo con id ..." |
| Buscar | Error | `test_buscar_error_id_no_numerico` | Excepción "entero" |
| Buscar | Error | `test_buscar_error_categoria_invalida` | Excepción "Categoría" |

## test/test_categoria.py – reglas de negocio, sin base de datos (19 pruebas)

- 10 normales: las 8 categorías, valor 0 y coma decimal (`1000,50`).
- 8 de error: valor vacío, texto, negativo, infinito, bolsas decimales, mililitros vacíos o
  negativos, categoría inválida.
- 1 de formato colombiano de pesos (`$19.000,00`).
