# Casos de prueba

Pruebas unitarias con `unittest` (36 en total). Se ejecutan con:

```
python -m unittest discover -s test -p "*test*.py" -v
```

## test/test_calculo.py: reglas del negocio, sin base de datos (24 pruebas)

| Tipo | Prueba | Qué verifica |
| --- | --- | --- |
| Normal | `test_normal_canasta` | 50000 en canasta básica: impuesto 0 |
| Normal | `test_normal_alimentos_5` | 100000 al 5%: 5000 |
| Normal | `test_normal_general_19` | 100000 al 19%: 19000 |
| Normal | `test_normal_restaurante` | 100000 al 8%: 8000 |
| Normal | `test_normal_licores` | 200000 al 49%: 98000 |
| Normal | `test_normal_suntuarios` | 100000 al 19%: 19000 |
| Normal | `test_normal_bolsas` | 10 bolsas x 73: 730 |
| Normal | `test_normal_cigarrillos` | 100000 x 0.30 + 10 ml x 2000: 50000 |
| Extraordinario | `test_extraordinario_valor_cero` | valor 0: impuesto 0 |
| Extraordinario | `test_extraordinario_coma_decimal` | "2,5" se entiende como 2.5 |
| Extraordinario | `test_extraordinario_valor_maximo` | el valor máximo permitido todavía se calcula |
| Extraordinario | `test_extraordinario_cigarrillos_sin_mililitros` | sin mililitros solo cobra el 30% |
| Extraordinario | `test_extraordinario_espacios_en_el_valor` | "  100000  " se acepta |
| Error | `test_error_valor_texto` | "abc" dispara `ErrorValorInvalido` |
| Error | `test_error_valor_vacio` | "" dispara `ErrorValorInvalido` |
| Error | `test_error_valor_negativo` | "-5" dispara `ErrorValorInvalido` |
| Error | `test_error_valor_demasiado_grande` | "1e30" dispara `ErrorValorInvalido` |
| Error | `test_error_valor_infinito` | "inf" dispara `ErrorValorInvalido` |
| Error | `test_error_valor_nan` | "nan" dispara `ErrorValorInvalido` |
| Error | `test_error_bolsas_con_decimales` | 2.5 bolsas dispara `ErrorValorInvalido` |
| Error | `test_error_mililitros_texto` | mililitros "abc" dispara `ErrorValorInvalido` |
| Error | `test_error_mililitros_negativos` | mililitros "-3" dispara `ErrorValorInvalido` |
| Error | `test_error_categoria_desconocida` | "zapatos" dispara `ErrorCategoriaDesconocida` |
| Error | `test_error_mensaje_dice_cual_fue_el_dato` | el mensaje de error incluye el dato escrito |

## test/test_calculos_controller.py: base de datos (12 pruebas)

Estas pruebas borran los cálculos de la base de datos que esté en `secret_config.py`. Usar una base de datos de pruebas.

| Funcionalidad | Prueba | Qué verifica |
| --- | --- | --- |
| Insertar | `test_insertar_y_buscar_por_id` | lo guardado se trae igual con el id |
| Insertar | `test_insertar_pone_id_y_fecha` | la base de datos le pone id y fecha |
| Insertar | `test_insertar_cigarrillos_guarda_los_mililitros` | se guardan los mililitros |
| Insertar | `test_insertar_bolsas` | 10 bolsas: impuesto 730 |
| Insertar | `test_dos_calculos_tienen_ids_diferentes` | los ids no se repiten |
| Buscar | `test_buscar_por_categoria` | solo trae los de esa categoría |
| Buscar | `test_buscar_por_categoria_sin_resultados` | lista vacía |
| Buscar | `test_buscar_todos` | trae los 3 guardados |
| Buscar | `test_buscar_todos_con_la_tabla_vacia` | lista vacía |
| Error | `test_error_buscar_id_que_no_existe` | un uuid que nadie tiene dispara `ErrorNoEncontrado` |
| Error | `test_error_buscar_id_que_no_es_un_uuid` | el texto "abc" dispara `ErrorNoEncontrado` |
| Crear tabla | `test_crear_tabla_dos_veces_no_falla` | crearla otra vez no da error ni borra datos |
