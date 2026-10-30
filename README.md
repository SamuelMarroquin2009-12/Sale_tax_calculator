# Sale_tax_calculator – Calculadora de impuestos de compra (Colombia)

Aplicación **web** en Python (Flask), con patrón **MVC** y Blueprints de Flask, y base de datos **PostgreSQL** (psycopg2). Calcula el impuesto de una compra según su categoría y **guarda y consulta** los cálculos en la base de datos. La versión de consola sigue disponible en la carpeta `src/view-console/`.

**Aplicación publicada:** https://sale-tax-calculator.onrender.com

## Autores (creadores del proyecto original)

| Integrante              | GitHub                                             |
| ----------------------- | -------------------------------------------------- |
| Isabella Ruiz Velasquez | [@IRVMakiAkame0](https://github.com/IRVMakiAkame0) |
| Samuel Marroquín        | [@SamuelMarroquin2009-12](https://github.com/SamuelMarroquin2009-12)   |

### Colaboración previa

- Juan Sebastián López: compilación para Windows y APK de Android. Ese trabajo fue retirado del proyecto a solicitud del docente.

## Funcionalidades de la aplicación web

| Opción del menú | Ruta | Qué hace |
| --------------- | ---- | -------- |
| Menú de inicio | `/` | Acceso a las funcionalidades principales |
| Guía de impuestos | `/guia/` | Explica en lenguaje sencillo cada impuesto, con un ejemplo calculado |
| Tablas de la BD | `/tablas/` | Permite consultar el estado de la tabla `calculos`, crearla o borrarla con confirmación |
| Calcular y guardar (Insertar) | `/calculos/nuevo` | Calcula el impuesto y guarda el cálculo en la base de datos |
| Buscar | `/calculos/buscar` | Busca por ID, por categoría o muestra todos los cálculos |

## Estructura (MVC con Blueprints de Flask)

```text
Sale_tax_calculator/
├── README.md
├── requirements.txt
├── secret_config_sample.py          # Plantilla de conexión, sin datos privados
├── sql/
│   ├── crear-calculos.sql           # Script para crear la tabla
│   └── borrar-calculos.sql          # Script para borrar la tabla
├── src/
│   ├── app.py                       # Crea Flask y registra los Blueprints
│   ├── model/                       # categoria.py, calculo.py, formato.py,
│   │                                # excepciones.py, guia_impuestos.py
│   ├── controller/
│   │   ├── calculos_controller.py   # Acceso a datos: tabla, insertar y buscar
│   │   ├── guia_controller.py       # Prepara los datos de la guía
│   │   └── blueprints/              # inicio.py, guia.py, calculos.py, tablas.py
│   ├── view-web/                    # Templates HTML y recursos CSS/JavaScript
│   └── view-console/                # Interfaz de usuario por consola
├── test/                            # Pruebas automatizadas con unittest
└── doc/                             # Casos de prueba y documentos del proyecto
```

## Guía rápida para quien evalúa (con su propia base de datos)

Esta guía resume cómo ejecutar la aplicación web en un computador con PostgreSQL. Los pasos se explican con más detalle en las secciones 1 a 5 de este README.

**Necesita:** Python 3.10 o superior, Git (o descargar el repositorio como ZIP desde GitHub) y PostgreSQL con su usuario y contraseña.

**1. Descargar el proyecto**

```bash
git clone https://github.com/SamuelMarroquin2009-12/Sale_tax_calculator.git
cd Sale_tax_calculator
```

**2. Crear y activar el entorno virtual**

En Linux o macOS, use `python3` si `python` no está disponible.

```bash
python -m venv .venv
```

```powershell
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
```

```bash
# Linux / macOS
source .venv/bin/activate
```

**3. Instalar las dependencias**

```bash
python -m pip install -r requirements.txt
```

**4. Crear una base de datos vacía en PostgreSQL**

En pgAdmin: clic derecho en *Databases* → *Create* → *Database* y use el nombre `ventas`.

O desde la consola:

```bash
psql -U postgres -c "CREATE DATABASE ventas;"
```

No hace falta crear la tabla manualmente: la aplicación permite crearla desde el menú **Tablas** y también puede crearla al guardar el primer cálculo cuando no existe.

**5. Configurar la conexión a la base de datos**

Copie la plantilla y edítela:

```powershell
# Windows
copy secret_config_sample.py secret_config.py
```

```bash
# Linux / macOS
cp secret_config_sample.py secret_config.py
```

Configure `secret_config.py` con los datos de **su propio servidor**, por ejemplo:

```python
PGHOST = "localhost"
PGDATABASE = "ventas"
PGUSER = "postgres"
PGPASSWORD = "su contraseña de PostgreSQL"
PGPORT = 5432
```

Use los datos reales de su instalación. No suba el archivo `secret_config.py` ni sus credenciales a GitHub.

**6. Ejecutar la aplicación web y abrirla**

```bash
python src/app.py
```

Abra en el navegador [http://127.0.0.1:5000](http://127.0.0.1:5000).

Para detener la aplicación, pulse `Ctrl + C` en la terminal.

Si el puerto 5000 está ocupado, puede probar con otro puerto:

```bash
# Linux / macOS
PORT=5001 python src/app.py
```

```powershell
# Windows (PowerShell)
$env:PORT=5001; python src/app.py
```

Después, abra [http://127.0.0.1:5001](http://127.0.0.1:5001). Esto requiere que la aplicación esté configurada para leer la variable `PORT`.

**7. Recorrer la aplicación**

Con la base de datos en blanco:

1. **Inicio:** permite acceder a las funciones principales.
2. **Calcular:** seleccione una categoría, escriba el valor y pulse **Calcular y guardar**. Esta función calcula y guarda el registro. Si la tabla no existe, la aplicación intenta crearla automáticamente.
3. **Tablas:** muestra el estado de la tabla y permite crearla o borrarla. La opción de borrado solicita escribir `SI` para confirmar.
4. **Buscar:** permite consultar por ID, por categoría o ver todos los cálculos guardados.
5. **Guía:** explica las categorías de impuestos y muestra ejemplos.

**8. Ejecutar las pruebas unitarias (opcional)**

Las pruebas pueden borrar y recrear la tabla `calculos`. Utilice una base de datos destinada exclusivamente a pruebas.

```bash
python -m unittest discover -s test -p "*test*.py" -v
```

En la última ejecución completa se obtuvieron **58 pruebas correctas (`OK`)**.

Si algo falla, consulte la sección **Solución de problemas** al final.

## Criterios de la entrega y dónde encontrarlos

| Criterio | Dónde está |
| -------- | ---------- |
| Funcionalidad web principal | Aplicación Flask: `src/app.py` y página **Calcular** (`/calculos/nuevo`) |
| Funcionalidad web para **Buscar** | Página **Buscar** (`/calculos/buscar`): `controller/blueprints/calculos.py` y métodos de búsqueda de `CalculosController` |
| Funcionalidad web para **Insertar** | Página **Calcular** (`/calculos/nuevo`): `controller/blueprints/calculos.py` y `CalculosController.insertar` |
| Menú de inicio | Página `/` y barra de navegación: Inicio, Guía, Calcular, Tablas y Buscar |
| Opción del menú para crear las tablas | Página **Tablas** (`/tablas/`) |
| Instrucciones en el README | Guía rápida y secciones 1 a 5 |
| Pruebas unitarias | Carpeta `test/` y sección 5 |
| Estructura MVC con Blueprints de Flask | `src/model/`, `src/view-web/` y `src/controller/blueprints/` |
| Aplicación publicada en la web | URL al inicio de este README y sección 6 |

## Prerrequisitos

- Python 3.10 o superior y Git, o descargar el repositorio como ZIP.
- Una base de datos PostgreSQL con sus datos de acceso. Puede instalarse en el computador para evaluar el proyecto o utilizarse un servicio en la nube como [Neon](https://neon.tech) o [Render](https://dashboard.render.com).

## 1. Instalación

Descargue el repositorio y entre a la carpeta del proyecto:

```bash
git clone https://github.com/SamuelMarroquin2009-12/Sale_tax_calculator.git
cd Sale_tax_calculator
python -m venv .venv
```

Active el entorno virtual:

```powershell
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
```

```bash
# Linux / macOS
source .venv/bin/activate
```

Instale las dependencias:

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

## 2. Crear la base de datos

El proyecto utiliza PostgreSQL. No incluye una base de datos propia: se conecta a la que se indique en `secret_config.py` o en las variables de entorno configuradas para el despliegue.

### Opción A – PostgreSQL instalado en el computador (recomendada para evaluar)

1. Con pgAdmin o `psql`, cree una base de datos vacía, por ejemplo, `ventas`.
2. Anote los datos de conexión:
   - Host: `localhost`.
   - Puerto: `5432`, o el que utilice su instalación.
   - Base de datos: `ventas`.
   - Usuario y contraseña de PostgreSQL.

Desde `psql`, puede crear la base de datos con:

```sql
CREATE DATABASE ventas;
```

### Opción B – Neon

1. Entre a [neon.tech](https://neon.tech) y cree una cuenta y un proyecto.
2. En el panel del proyecto, abra los datos de conexión (*Connection Details*).
3. Copie el host, el nombre de la base de datos, el usuario, la contraseña y el puerto.

### Opción C – Render PostgreSQL

1. Entre a [Render](https://dashboard.render.com).
2. Seleccione **New +** → **PostgreSQL**.
3. Cree la base de datos y consulte los datos de conexión.
4. Para conectarse desde un servicio externo, utilice los datos de conexión **External**.

En Render, el host interno solo funciona desde servicios que tengan acceso a la red interna correspondiente.

## 3. Configurar la conexión

Los datos de conexión se guardan en `secret_config.py`, que no debe subirse a GitHub. El repositorio incluye `secret_config_sample.py` como plantilla.

Copie el archivo:

```powershell
# Windows
copy secret_config_sample.py secret_config.py
```

```bash
# Linux / macOS
cp secret_config_sample.py secret_config.py
```

Abra `secret_config.py` y reemplace `PGHOST`, `PGDATABASE`, `PGUSER`, `PGPASSWORD` y `PGPORT` con los datos de su base de datos.

**Nota para quien evalúe:** `secret_config.py` contiene credenciales privadas y no debe compartirse en el repositorio. Cada persona debe crear su propia base de datos y configurar su conexión.

La aplicación permite crear la tabla desde el menú **Tablas** o automáticamente al guardar el primer cálculo, cuando corresponda. La versión de consola también incluye herramientas para administrar la tabla.

**Importante:** las pruebas pueden borrar y recrear la tabla `calculos`. Ejecútelas únicamente contra una base de datos de pruebas.

## 4. Ejecutar la aplicación web

Con el entorno virtual activado y la conexión configurada, desde la carpeta raíz del proyecto ejecute:

```bash
python src/app.py
```

Abra [http://127.0.0.1:5000](http://127.0.0.1:5000) en el navegador.

Se recomienda probar las funciones en este orden:

1. Entre a **Tablas** y compruebe el estado de la tabla. Si es necesario, pulse **Crear tablas**.
2. Entre a **Calcular y guardar**, seleccione una categoría, escriba el valor y realice un cálculo.
3. Entre a **Buscar** para consultar por ID, por categoría o todos los registros.
4. Consulte la **Guía** para revisar las categorías y los ejemplos.

La opción **Borrar tablas** elimina la tabla y solicita escribir `SI` para confirmar. Úsela con cuidado, especialmente si la base de datos contiene información que desea conservar.

### Versión de consola (opcional)

La versión de consola sigue disponible en `src/view-console/`. Los siguientes comandos corresponden a los scripts descritos en el proyecto:

```bash
python src/view-console/crear_tablas.py
python src/view-console/crear_calculo.py
python src/view-console/buscar_calculo.py
python src/view-console/borrar_tablas.py
```

Estos scripts permiten crear la tabla, calcular y guardar un impuesto, buscar cálculos y borrar la tabla, respectivamente.

## 5. Ejecutar las pruebas unitarias

Las pruebas se ejecutan con `unittest` y verifican distintas partes del modelo, los controladores y la aplicación web.

Ejecute:

```bash
python -m unittest discover -s test -p "*test*.py" -v
```

**Resultado verificado:** 58 pruebas ejecutadas correctamente (`OK`).

Las pruebas incluyen comprobaciones de la guía, la navegación, las rutas web, las validaciones de entrada y las operaciones de cálculo y consulta.

**Advertencia sobre la base de datos:** algunas pruebas utilizan preparaciones (`setUp` y `setUpClass`) que borran y crean la tabla `calculos`. Por lo tanto, utilice una base de datos exclusiva para pruebas. No ejecute la suite contra una base de datos de producción ni contra una base que contenga datos que deba conservar.

El tiempo de ejecución puede variar según la conexión y la configuración de PostgreSQL.

## 6. Publicar la aplicación en la web (Render)

La aplicación puede desplegarse en un servicio web de Render y conectarse a una base de datos PostgreSQL alojada en un servicio compatible.

1. Suba el repositorio a GitHub. Asegúrese de no incluir `secret_config.py` ni credenciales.
2. Entre a [Render](https://dashboard.render.com) y seleccione **New +** → **Web Service**.
3. Conecte el repositorio.
4. Configure el comando de construcción (*Build Command*):

   ```bash
   pip install -r requirements.txt
   ```

5. Configure el comando de inicio (*Start Command*):

   ```bash
   gunicorn --chdir src app:app
   ```

6. En las variables de entorno del servicio, configure los datos de conexión que necesita la aplicación: `PGHOST`, `PGDATABASE`, `PGUSER`, `PGPASSWORD` y `PGPORT`. Configure también `SECRET_KEY` si la aplicación la requiere.
7. Cree el servicio y revise los registros de inicio.
8. Cuando el despliegue termine, abra la URL pública y compruebe que las páginas principales carguen correctamente.

La base de datos debe existir y estar accesible desde el servicio web. Si la tabla no existe, créela desde el menú **Tablas** o guarde el primer cálculo si la creación automática está disponible.

Finalmente, reemplace el marcador de **Aplicación publicada** al inicio de este README por la URL real de la aplicación desplegada.

## Modelo de datos

La tabla `calculos` almacena los cálculos realizados. El script `sql/crear-calculos.sql` contiene la definición de la tabla.

| Columna | Tipo | Descripción |
| ------- | ---- | ----------- |
| `id_calculo` | `serial`, llave primaria | Identificador del cálculo |
| `categoria` | `varchar(20)` | Clave de la categoría seleccionada |
| `valor` | `decimal` | Valor de la compra o cantidad de bolsas, según la categoría |
| `mililitros` | `decimal` | Dato utilizado en la categoría de cigarrillos/vapeadores |
| `impuesto` | `decimal` | Impuesto calculado |
| `fecha` | `timestamp` | Fecha y hora del registro |

Clases principales del modelo:

- `Categoria`: representa las categorías y sus reglas de cálculo.
- `Calculo`: representa un cálculo de impuesto y sus datos.

## Entradas y fórmulas

Las siguientes fórmulas resumen las reglas configuradas en el proyecto:

| Categoría | Dato de entrada | Fórmula |
| --------- | --------------- | ------- |
| Canasta básica / Exento | Valor (COP) | `valor × 0` |
| Alimentos con IVA 5 % | Valor (COP) | `valor × 0.05` |
| Bienes generales IVA 19 % | Valor (COP) | `valor × 0.19` |
| Restaurantes (INC 8 %) | Valor (COP) | `valor × 0.08` |
| Licores | Valor (COP) | `valor × 0.49` |
| Bienes suntuarios | Valor (COP) | `valor × 0.19` |
| Bolsas plásticas | Cantidad de bolsas | `cantidad × 73` |
| Cigarrillos / Vapeadores | Valor (COP) y mililitros | `(valor × 0.30) + (ml × 2000)` |

Los números deben escribirse **sin separador de miles**; por ejemplo, `50000`, no `50.000`.

Las tarifas y fórmulas anteriores reflejan la lógica implementada en el proyecto académico. Para determinar las obligaciones tributarias aplicables a una compra real, se debe consultar la normativa colombiana vigente.

## Salidas

- **Caso exitoso:** muestra el impuesto calculado y, cuando corresponde, el identificador del registro guardado.
- **Caso de error:** presenta un mensaje que ayuda a identificar el problema, como un valor vacío, negativo o no numérico, una categoría inválida, un ID inexistente, una tabla que no existe o un problema de conexión.

Los errores previstos se manejan mediante excepciones propias definidas en `src/model/excepciones.py`, entre ellas:

- `ErrorCalculadora`
- `ErrorValorInvalido`
- `ErrorCategoriaDesconocida`
- `ErrorNoEncontrado`
- `ErrorBaseDeDatos`
- `ErrorTablaNoExiste`
- `ErrorConexion`
- `ErrorConfiguracion`

## Casos de prueba

Consulte [`doc/casos_de_prueba.md`](doc/casos_de_prueba.md) para revisar los casos documentados.

La suite automatizada incluye pruebas de las funcionalidades del proyecto y de los comportamientos de error. El comando para ejecutar todas las pruebas se encuentra en la sección 5.

## Solución de problemas

- **Faltan datos de conexión:** copie `secret_config_sample.py` como `secret_config.py` y complete los datos de su base de datos, o configure las variables de entorno requeridas por el despliegue.
- **No se pudo conectar a PostgreSQL:** revise `PGHOST`, `PGDATABASE`, `PGUSER`, `PGPASSWORD` y `PGPORT`. Compruebe que el servidor esté disponible y que el usuario tenga permisos.
- **La tabla `calculos` no existe:** entre a **Tablas** en la aplicación web y utilice **Crear tablas**, o ejecute `python src/view-console/crear_tablas.py`.
- **Falta una dependencia:** active el entorno virtual e instale las dependencias con `python -m pip install -r requirements.txt`.
- **`ModuleNotFoundError: No module named 'flask'` o `psycopg2`:** compruebe que el entorno virtual esté activado y que las dependencias se hayan instalado correctamente.
- **PowerShell bloquea `Activate.ps1`:** si la política de ejecución lo permite en su equipo, puede ejecutar `Set-ExecutionPolicy -Scope Process Bypass` en esa sesión y volver a activar el entorno.
- **`password authentication failed` o `database "ventas" does not exist`:** revise el usuario, la contraseña y el nombre de la base de datos configurados.
- **`Address already in use`:** el puerto está ocupado. Configure otro puerto si la aplicación admite la variable `PORT`.
- **El despliegue en Render no inicia:** revise los registros del servicio, el comando de inicio y las variables de entorno.

## Notas

Las tarifas de la tabla de fórmulas corresponden a la implementación del proyecto y pueden modificarse en el código del modelo, especialmente en `src/model/categoria.py`. No deben interpretarse como una certificación de las tarifas tributarias oficiales vigentes.
