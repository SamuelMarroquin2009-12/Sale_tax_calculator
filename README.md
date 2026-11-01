# Sale_tax_calculator

Aplicación web que calcula el impuesto de una compra en Colombia, lo guarda en una base de datos PostgreSQL y permite buscar lo que se guardó. Está hecha con Flask y el patrón MVC (con Blueprints).

**Aplicación publicada:** https://sale-tax-calculator-eo97.onrender.com

## Integrantes

- Isabella Ruiz Velasquez
- Samuel Marroquín

## Las dos versiones de la página web

La aplicación tiene dos páginas web que usan el mismo Model y el mismo Controller, solo cambia cómo se ven:

| Versión | Dirección | Qué es |
| --- | --- | --- |
| Simple (la que se presenta) | `/` | HTML básico: menú, calcular, buscar y crear tablas |
| Completa | `/completa/` | La versión visual de Isabella: colores, iconos, guía de impuestos y modo oscuro |

Desde el menú de la versión simple hay un enlace a la completa, y en el pie de la completa hay uno de regreso.

## Entradas, proceso y salidas

- **Entradas:** el tipo de producto, el valor de la compra (o la cantidad de bolsas) y los mililitros, que solo se usan en cigarrillos y vapeadores.
- **Proceso:** se revisa que lo escrito sea un número válido y se aplica la fórmula del tipo de producto.
- **Salidas:** el impuesto a pagar, guardado con su id y su fecha. Si algo está mal escrito sale un mensaje que explica qué pasó.

| Tipo de producto | Fórmula |
| --- | --- |
| Canasta básica / Exento | valor x 0 |
| Alimentos con IVA 5% | valor x 0.05 |
| Bienes generales IVA 19% | valor x 0.19 |
| Restaurantes (INC 8%) | valor x 0.08 |
| Licores | valor x 0.49 |
| Bienes suntuarios | valor x 0.19 |
| Bolsas plásticas | cantidad x 73 |
| Cigarrillos / Vapeadores | (valor x 0.30) + (mililitros x 2000) |

Los números se escriben sin puntos de miles (50000, no 50.000). El valor máximo es 999999999999. Estas tarifas son las del proyecto académico, no son una certificación oficial.

## Estructura del proyecto (MVC)

```
Sale_tax_calculator/
├── app.py                     # crea la aplicación Flask y registra el Blueprint
├── requirements.txt
├── secret_config_sample.py    # plantilla de los datos de la base de datos
├── sql/
│   ├── crear-calculos.sql     # crea la tabla calculos
│   └── borrar-calculos.sql    # borra la tabla (solo la versión completa lo usa)
├── src/
│   ├── model/                 # reglas del negocio: calculo.py (y formato.py para mostrar pesos)
│   ├── controller/            # acceso a la base de datos: calculos_controller.py y tablas_controller.py
│   └── view/web/              # los Blueprints: vista_calculos.py (simple) y vista_completa.py (completa)
├── templates/                 # páginas HTML de la versión simple
│   └── completa/              # páginas HTML de la versión completa
├── static/completa/           # estilos, modo oscuro y scripts de la versión completa
├── test/                      # pruebas unitarias
└── doc/                       # casos de prueba y documentos
```

## Cómo ejecutarla en mi computador (con una base de datos en blanco)

1. Instale Python 3 y tenga una base de datos PostgreSQL vacía (en el computador, o una gratis en https://neon.tech o https://render.com).
2. Descargue el proyecto y entre a la carpeta:

```
git clone https://github.com/SamuelMarroquin2009-12/Sale_tax_calculator.git
cd Sale_tax_calculator
```

3. Instale las dependencias:

```
pip install -r requirements.txt
```

4. Copie `secret_config_sample.py` con el nombre `secret_config.py` y escriba adentro los datos de su base de datos. Ese archivo no se sube a GitHub.

```
copy secret_config_sample.py secret_config.py
```

(en Linux o Mac es `cp secret_config_sample.py secret_config.py`)

5. Ejecute la aplicación:

```
python app.py
```

6. Abra http://127.0.0.1:5000 en el navegador (la versión completa está en http://127.0.0.1:5000/completa/).
7. Como la base de datos está en blanco, lo primero es entrar a **Crear las tablas de la base de datos** en el menú. Después ya puede calcular y buscar. (La versión completa además crea la tabla sola al guardar el primer cálculo.)

## Pruebas unitarias

```
python -m unittest discover -s test -p "*test*.py" -v
```

OJO: las pruebas del controlador borran todos los cálculos de la base de datos que esté en `secret_config.py`. Úselas con una base de datos de pruebas.

## Publicar en Render

- Build Command: `pip install -r requirements.txt`
- Start Command: `flask run -p 10000 -h 0.0.0.0`
- En Environment agregue las variables `PGHOST`, `PGDATABASE`, `PGUSER`, `PGPASSWORD` y `PGPORT` con los datos de la base de datos.
- Opcionales: `APP_ENV=production` desactiva el botón de borrar tablas de la versión completa (para no perder los datos publicados) y `SECRET_KEY` es la clave que usa Flask para los avisos de esa versión.

## Problemas comunes

- **Sale un mensaje de problema con la base de datos:** revise los datos de `secret_config.py` y que haya pulsado **Crear las tablas** en el menú.
- **ModuleNotFoundError:** falta instalar las dependencias (paso 3).
- **El puerto 5000 está ocupado:** cierre el programa que lo usa o ejecute `flask run -p 5001`.
