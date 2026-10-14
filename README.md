[README.md](https://github.com/user-attachments/files/33416797/README.md)
# Sale_tax_calculator – Calculadora de impuestos de compra (Colombia)

Aplicación de **consola** en Python que calcula el impuesto de una compra según su categoría
(IVA / INC vigentes en Colombia) y **guarda y consulta** los cálculos en una base de datos
PostgreSQL usando el ORM **Peewee**.

## Integrantes

- Samuel Marroquín
- Isabella Ruiz Velasquez

## Estructura

```
Sale_tax_calculator/
├── main.py                    # punto de entrada
├── secret_config_sample.py    # plantilla de conexión (sin datos privados)
├── requirements.txt
├── pytest.ini
├── src/
│   ├── model/                 # database.py, models.py (ORM), calculadora.py, formato.py
│   ├── controller/            # controller.py (crear/borrar tablas, insertar, buscar)
│   └── view/                  # consola.py (interfaz de usuario)
├── tests/                     # conftest.py (fixtures) y pruebas
└── doc/                       # casos_de_prueba.md
```

## Requisitos

- Python 3.10 o superior
- Una base de datos PostgreSQL (se usó la de [Render](https://dashboard.render.com))

## 1. Instalación

```bash
git clone https://github.com/SamuelMarroquin2009-12/Sale_tax_calculator.git
cd Sale_tax_calculator
python -m venv venv
```

Activar el entorno virtual:

```bash
# Windows (PowerShell)
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

Instalar dependencias:

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

## 2. Crear la base de datos (Render)

1. Entra a <https://dashboard.render.com> → **New +** → **PostgreSQL**.
2. Ponle un nombre, elige el plan gratuito y pulsa **Create Database**.
3. Cuando termine de crearse, abre la base de datos y en la sección **Connections** copia los
   datos **External**: Hostname (termina en `.render.com`), Port, Database, Username y Password.

## 3. Configurar la conexión

Los datos de conexión van en `secret_config.py`, que **no se sube a GitHub** (está en
`.gitignore`). El repositorio solo incluye `secret_config_sample.py` con valores de ejemplo.

```bash
# Windows
copy secret_config_sample.py secret_config.py
# Linux / macOS
cp secret_config_sample.py secret_config.py
```

Abre `secret_config.py` y reemplaza `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` y `DB_PASSWORD`
con los datos copiados de Render.

> Si `secret_config.py` no existe o la conexión falla, el programa no se cae: avisa y usa una
> base SQLite local (`~/.sale_tax_calculator/calculadora.db`) para que siga funcionando.

## 4. Ejecutar el programa

```bash
python main.py
```

Al iniciar, el programa conecta con la base de datos y crea las tablas si no existen. Menú:

| Opción | Acción |
| ------ | ------ |
| 1 | Crear las tablas (`CREATE TABLE`) y cargar las 8 categorías |
| 2 | Borrar las tablas (`DROP TABLE`) |
| 3 | Calcular y guardar un cálculo (`INSERT INTO`) |
| 4 | Buscar cálculos por categoría o por id (`SELECT`) |
| 5 | Calcular sin guardar |
| 0 | Salir |

Después de borrar las tablas (opción 2), usa la opción 1 para recrearlas.

## 5. Ejecutar las pruebas

Las pruebas usan una base SQLite en memoria (un *fixture* crea y borra las tablas en cada
prueba), así que **no necesitan** `secret_config.py` ni internet:

```bash
pytest -v
```

Resultado esperado: `49 passed`.

## Modelo de datos (ORM)

- **Categoria**: `id`, `clave` (única), `nombre`, `formula`.
- **Calculo**: `id`, `categoria` (FK → Categoria), `valor`, `mililitros`, `impuesto`, `creado`.

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

- **Caso exitoso:** el impuesto en pesos colombianos (ej. `$19.000,00`), y si se guardó, su id.
- **Caso de error:** mensaje claro (valor negativo, no numérico, categoría inválida, id
  inexistente, tablas sin crear). El programa no se cierra: vuelve al menú.

## Casos de prueba

Ver [`doc/casos_de_prueba.md`](doc/casos_de_prueba.md). Cada funcionalidad (crear/borrar tablas,
insertar, buscar) tiene al menos un caso normal y uno de error.

## Solución de problemas

- *Error `'NoneType' object has no attribute 'endswith'` al instalar:* ejecuta
  `python -m pip install --upgrade pip setuptools wheel` y vuelve a instalar.
- *Dice "se usa la base local":* falta `secret_config.py` o los datos de Render son incorrectos.
- *Error de conexión por hostname:* usa el hostname **External** (termina en `.render.com`).
- *Las bases gratuitas de Render caducan:* si la tuya expira, crea otra y actualiza `secret_config.py`.

## Notas

Las tarifas de IVA e INC corresponden a la normativa tributaria colombiana vigente y pueden
actualizarse en `src/model/calculadora.py`.
