# Sale_tax_calculator – Calculadora de impuestos de compra (Colombia)

Aplicación de consola en Python, con patrón **MVC** y base de datos **PostgreSQL** (psycopg2),
que calcula el impuesto de una compra según su categoría (IVA / INC vigentes en Colombia) y
**guarda y consulta** los cálculos en la base de datos.

## Integrantes

- Samuel Marroquín
- Isabella Ruiz Velasquez

## Estructura

```
Sale_tax_calculator/
├── README.md
├── requirements.txt
├── secret_config_sample.py          # plantilla de conexión (sin datos privados)
├── sql/
│   ├── crear-calculos.sql           # script que crea la tabla
│   └── borrar-calculos.sql          # script que borra la tabla
├── src/
│   ├── model/                       # categoria.py, calculo.py (clases Model), formato.py
│   ├── controller/                  # calculos_controller.py (crear/borrar tabla, insertar, buscar)
│   └── view-console/                # interfaz de usuario por consola
├── test/                            # pruebas unitarias (unittest) con test fixtures
└── doc/                             # casos_de_prueba.md y documentos del proyecto
```

## Prerrequisitos

- Python 3.10 o superior
- Una base de datos PostgreSQL con sus datos de acceso (se usó la de [Render](https://dashboard.render.com))

## 1. Instalación

```bash
git clone https://github.com/SamuelMarroquin2009-12/Sale_tax_calculator.git
cd Sale_tax_calculator
python -m venv .venv
```

Activar el entorno virtual:

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Linux / macOS
source .venv/bin/activate
```

Instalar el paquete psycopg2:

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

## 2. Crear la base de datos (Render)

1. Entre a <https://dashboard.render.com> → **New +** → **PostgreSQL**.
2. Póngale un nombre, elija el plan gratuito y pulse **Create Database**.
3. Cuando termine de crearse, abra la base de datos y en la sección **Connections** copie los
   datos **External**: Hostname (termina en `.render.com`), Port, Database, Username y Password.

## 3. Configurar la conexión

Los datos de conexión van en `secret_config.py`, que **no se sube a GitHub** (está en
`.gitignore`). El repositorio solo incluye `secret_config_sample.py`, con instrucciones de uso.

```bash
# Windows
copy secret_config_sample.py secret_config.py
# Linux / macOS
cp secret_config_sample.py secret_config.py
```

Abra `secret_config.py` y reemplace `PGHOST`, `PGDATABASE`, `PGUSER`, `PGPASSWORD` y `PGPORT`
con los datos copiados de Render.

> **Nota para quien evalúe:** `secret_config.py` contiene credenciales privadas y por eso no
> está en el repositorio. Cree su propia base de datos (paso 2) y llene `secret_config.py`
> con sus datos (paso 3). Si algo falla, el programa muestra un mensaje que indica qué revisar.

## 4. Ejecutar el programa

Desde la carpeta del proyecto, cada acción es un script de la consola:

```bash
python src/view-console/crear_tablas.py     # crea la tabla calculos (CREATE TABLE)
python src/view-console/crear_calculo.py    # calcula el impuesto y lo guarda (INSERT INTO)
python src/view-console/buscar_calculo.py   # busca por id, por categoría o todos (SELECT)
python src/view-console/borrar_tablas.py    # borra la tabla calculos (DROP TABLE)
```

**La primera vez, ejecute `crear_tablas.py` antes de insertar o buscar.**

## 5. Ejecutar las pruebas unitarias

Las pruebas usan la base de datos configurada en `secret_config.py`. Los *test fixtures*
(`setUpClass` y `setUp`) borran y crean la tabla `calculos` solos, así que **use una base de
pruebas: al correrlas se borran los cálculos guardados**.

```bash
python -m unittest discover -s test -p "*test*.py" -v
```

Resultado esperado: `Ran 39 tests ... OK`. En VS Code también se pueden correr desde el panel
*Testing* (ya está configurado en `.vscode/settings.json`).

## Modelo de datos

Tabla `calculos` (script `sql/crear-calculos.sql`):

| Columna | Tipo | Descripción |
| ------- | ---- | ----------- |
| id_calculo | serial, llave primaria | Identificador del cálculo |
| categoria | varchar(20) | Clave de la categoría (ej. `licores`) |
| valor | decimal | Valor de la compra o cantidad de bolsas |
| mililitros | decimal | Solo para cigarrillos / vapeadores |
| impuesto | decimal | Impuesto calculado |
| fecha | timestamp | Fecha y hora en que se guardó |

Clases del Model: `Categoria` (reglas y fórmula de cada categoría) y `Calculo` (un cálculo guardado).

## Entradas y fórmulas

| Categoría | Dato de entrada | Fórmula |
| --------- | --------------- | ------- |
| Canasta básica / Exento | Valor (COP) | `valor × 0` |
| Alimentos con IVA 5 % | Valor (COP) | `valor × 0.05` |
| Bienes generales IVA 19 % | Valor (COP) | `valor × 0.19` |
| Restaurantes (INC 8 %) | Valor (COP) | `valor × 0.08` |
| Licores | Valor (COP) | `valor × 0.49` |
| Bienes suntuarios | Valor (COP) | `valor × 0.19` |
| Bolsas plásticas | Cantidad (entero) | `cantidad × 73` |
| Cigarrillos / Vapeadores | Valor (COP) + mililitros | `(valor × 0.30) + (ml × 2000)` |

Los números se escriben **sin separador de miles** (ej. `50000`, no `50.000`).

## Salidas

- **Caso exitoso:** el impuesto en pesos colombianos (ej. `$19.000,00`) y el id con que se guardó.
- **Caso de error:** mensaje con la causa (valor vacío, negativo o no numérico, categoría inválida,
  id inexistente, tabla sin crear, sin conexión). El script termina sin mostrar errores técnicos.

## Casos de prueba

Ver [`doc/casos_de_prueba.md`](doc/casos_de_prueba.md). Cada funcionalidad (crear/borrar tabla,
insertar, buscar) tiene al menos un caso normal y uno de error.

## Solución de problemas

- *`No se encontró secret_config.py`:* copie `secret_config_sample.py` como `secret_config.py`
  en la misma carpeta que este README (paso 3).
- *`No se pudo conectar a la base de datos`:* revise los datos de `secret_config.py`; use el
  Hostname **External** (termina en `.render.com`).
- *`La tabla 'calculos' no existe`:* ejecute `python src/view-console/crear_tablas.py`.
- *Error `'NoneType' object has no attribute 'endswith'` al instalar:* ejecute
  `python -m pip install --upgrade pip setuptools wheel` y vuelva a instalar.
- *Las bases gratuitas de Render caducan:* si la suya expira, cree otra y actualice `secret_config.py`.

## Notas

Las tarifas de IVA e INC corresponden a la normativa tributaria colombiana vigente y pueden
actualizarse en `src/model/categoria.py`.
