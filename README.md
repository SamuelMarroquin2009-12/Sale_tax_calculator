# Sale_tax_calculator

Esta es una aplicación web que hicimos para el curso de Código Limpio. Calcula el impuesto de una compra en Colombia (IVA, consumo, bolsas, etc.), guarda cada cálculo en una base de datos PostgreSQL y después se pueden buscar los cálculos guardados. Está hecha con Flask y siguiendo el patrón MVC con Blueprints.

**La aplicación publicada está aquí:** https://sale-tax-calculator-eo97.onrender.com

Integrantes: Isabella Ruiz Velasquez y Samuel Marroquín.

## Cómo funciona

Uno escoge el tipo de producto, escribe el valor de la compra y la aplicación calcula el impuesto. Si es cigarrillos o vapeadores también hay que escribir los mililitros, y si son bolsas plásticas en vez del valor se escribe la cantidad de bolsas. Si algo se escribe mal (por ejemplo letras en vez de un número) sale un mensaje que explica qué fue lo que pasó.

Las fórmulas que usamos son estas:

| Tipo de producto | Impuesto |
| --- | --- |
| Canasta básica / Exento | valor x 0 |
| Alimentos con IVA 5% | valor x 0.05 |
| Bienes generales IVA 19% | valor x 0.19 |
| Restaurantes (INC 8%) | valor x 0.08 |
| Licores | valor x 0.49 |
| Bienes suntuarios | valor x 0.19 |
| Bolsas plásticas | cantidad x 73 |
| Cigarrillos / Vapeadores | (valor x 0.30) + (mililitros x 2000) |

Los números se escriben sin puntos de miles (50000, no 50.000) y el valor máximo que acepta es 999999999999. Estas tarifas son las de nuestro proyecto académico, no son una certificación oficial.

## Cómo está organizado el proyecto

Seguimos el patrón MVC, cada carpeta tiene su propio trabajo:

- `src/model/calculo.py` (Model): las reglas del negocio. Aquí está la clase `Calculo` que calcula el impuesto y los errores que pueden pasar. No usa ni Flask ni la base de datos.
- `src/controller/calculos_controller.py` (Controller): es el único que habla con la base de datos. Crea la tabla, guarda cálculos y los busca.
- `src/view/web/vista_calculos.py` (View): el Blueprint de Flask con todas las páginas. Recibe lo que escribe el usuario, le pide el trabajo al Model y al Controller y muestra el resultado.
- `templates/`: las páginas HTML.
- `sql/crear-calculos.sql`: el script que crea la tabla `calculos`.
- `test/`: las pruebas unitarias.
- `app.py`: crea la aplicación Flask y registra el Blueprint.

Además hay una carpeta `static/diseno/` con una maqueta que solo se ve bonita (ver más abajo). No hace parte de la aplicación que funciona.

## Cómo ejecutarla en su computador (con una base de datos en blanco)

1. Necesita tener Python 3 y una base de datos PostgreSQL vacía. Puede ser una de su computador o una gratis en https://neon.tech o https://render.com.
2. Descargue el proyecto y entre a la carpeta:

```
git clone https://github.com/SamuelMarroquin2009-12/Sale_tax_calculator.git
cd Sale_tax_calculator
```

3. Instale las librerías que necesita el proyecto:

```
pip install -r requirements.txt
```

4. Copie el archivo `secret_config_sample.py` con el nombre `secret_config.py` y escriba adentro los datos de su base de datos. Ese archivo está en el `.gitignore`, por eso no se sube a GitHub.

```
copy secret_config_sample.py secret_config.py
```

(en Linux o Mac el comando es `cp secret_config_sample.py secret_config.py`)

5. Ejecute la aplicación:

```
python app.py
```

6. Abra http://127.0.0.1:5000 en el navegador.
7. Como la base de datos está en blanco, lo primero que hay que hacer es entrar a **Crear las tablas de la base de datos** en el menú. Después ya se puede calcular y buscar.

## Pruebas unitarias

```
python -m unittest discover -s test -p "*test*.py" -v
```

Ojo: las pruebas del controlador borran los cálculos de la base de datos que esté en `secret_config.py`, entonces úselas con una base de datos de pruebas y nunca con la de verdad.

## Publicarla en Render

- Build Command: `pip install -r requirements.txt`
- Start Command: `flask run -p 10000 -h 0.0.0.0`
- En Environment hay que crear las variables `PGHOST`, `PGDATABASE`, `PGUSER`, `PGPASSWORD` y `PGPORT` con los datos de la base de datos.

## La maqueta visual

Antes de rehacer el proyecto con lo que vimos en clase, Isabella había hecho una página con más diseño (colores, iconos, modo oscuro y una guía de impuestos). La dejamos como maqueta: se puede navegar entre los apartados y apretar los botones, pero no calcula ni guarda nada. Se abre con la aplicación corriendo en http://127.0.0.1:5000/static/diseno/index.html (o en la dirección de Render, agregando `/static/diseno/index.html`).

## Problemas comunes

- **`flask` no se reconoce como comando:** todavía no se instalaron las librerías (paso 3), o Python no está en el PATH. Se puede ejecutar con `python app.py` y funciona igual.
- **Sale un mensaje de problema con la base de datos:** revise los datos de `secret_config.py` y que ya haya pulsado **Crear las tablas** en el menú.
- **ModuleNotFoundError:** faltan las librerías, haga el paso 3.
- **El puerto 5000 está ocupado:** cierre el programa que lo usa o ejecute `python -m flask run -p 5001`.
