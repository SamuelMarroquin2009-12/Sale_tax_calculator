import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.append(str(RAIZ))          # para encontrar secret_config.py
sys.path.append(str(RAIZ / "src"))  # para encontrar los paquetes model y controller

import psycopg2
import psycopg2.errors

from model.calculo import Calculo
from model.categoria import Categoria


class CalculosController:
    """
    Pertenece a la Capa de Controlador

    Crea y borra la tabla calculos, e inserta y busca Calculos en la base de datos PostgreSQL
    """

    @staticmethod
    def crear_tabla():
        """ Crea la tabla calculos ejecutando el script sql/crear-calculos.sql """
        CalculosController._ejecutar_script("crear-calculos.sql")

    @staticmethod
    def borrar_tabla():
        """ Borra la tabla calculos ejecutando el script sql/borrar-calculos.sql """
        CalculosController._ejecutar_script("borrar-calculos.sql")

    @staticmethod
    def borrar_filas():
        """ Borra todos los calculos guardados, pero deja la tabla """
        CalculosController._ejecutar("delete from calculos")

    @staticmethod
    def insertar(calculo: Calculo) -> int:
        """ Recibe una instancia de la clase Calculo, la inserta en la tabla y retorna su id """
        fila = CalculosController._ejecutar(
            """insert into calculos (categoria, valor, mililitros, impuesto)
               values (%s, %s, %s, %s)
               returning id_calculo, fecha""",
            (calculo.categoria, calculo.valor, calculo.mililitros, calculo.impuesto),
            traer="uno")
        calculo.id_calculo, calculo.fecha = fila
        return calculo.id_calculo

    @staticmethod
    def buscar_calculo(id_calculo) -> Calculo:
        """ Trae un calculo dado su id. Dispara una excepcion si no existe """
        try:
            id_calculo = int(id_calculo)
        except (TypeError, ValueError):
            raise ValueError("El id debe ser un número entero") from None

        fila = CalculosController._ejecutar(
            """select id_calculo, categoria, valor, mililitros, impuesto, fecha
               from calculos where id_calculo = %s""",
            (id_calculo,), traer="uno")
        if fila is None:
            raise ValueError(f"No existe un cálculo con id {id_calculo}")
        return CalculosController._a_calculo(fila)

    @staticmethod
    def buscar_por_categoria(categoria: str) -> list:
        """ Trae todos los calculos de una categoria """
        Categoria.obtener(categoria)  # dispara una excepcion si la categoria no existe
        filas = CalculosController._ejecutar(
            """select id_calculo, categoria, valor, mililitros, impuesto, fecha
               from calculos where categoria = %s order by id_calculo""",
            (categoria,), traer="todos")
        return [CalculosController._a_calculo(fila) for fila in filas]

    @staticmethod
    def buscar_todos() -> list:
        """ Trae todos los calculos guardados """
        filas = CalculosController._ejecutar(
            """select id_calculo, categoria, valor, mililitros, impuesto, fecha
               from calculos order by id_calculo""",
            traer="todos")
        return [CalculosController._a_calculo(fila) for fila in filas]

    @staticmethod
    def _a_calculo(fila) -> Calculo:
        return Calculo(id_calculo=fila[0], categoria=fila[1], valor=fila[2],
                       mililitros=fila[3], impuesto=fila[4], fecha=fila[5])

    @staticmethod
    def _ejecutar_script(nombre_archivo: str):
        with open(RAIZ / "sql" / nombre_archivo, "r", encoding="utf-8") as archivo:
            consulta = archivo.read()
        CalculosController._ejecutar(consulta)

    @staticmethod
    def _ejecutar(consulta: str, parametros=None, traer=None):
        """ Ejecuta una consulta, confirma los cambios y cierra la conexion """
        cursor = CalculosController.obtener_cursor()
        try:
            cursor.execute(consulta, parametros)
            resultado = None
            if traer == "uno":
                resultado = cursor.fetchone()
            elif traer == "todos":
                resultado = cursor.fetchall()
            # Todas las instrucciones que modifiquen la BD necesitan un commit para confirmar los cambios
            cursor.connection.commit()
            return resultado
        except psycopg2.errors.UndefinedTable as error:
            raise Exception("La tabla 'calculos' no existe. Ejecute crear_tablas.py para crearla.") from error
        except psycopg2.Error as error:
            raise Exception(f"Error de base de datos: {str(error).strip()}") from error
        finally:
            cursor.connection.close()

    @staticmethod
    def obtener_cursor():
        """ Crea la conexion a la base de datos y retorna un cursor para hacer consultas """
        try:
            import secret_config
        except ImportError as error:
            raise Exception("No se encontró secret_config.py. Copie secret_config_sample.py "
                            "como secret_config.py y ponga los datos de su base de datos "
                            "(vea el README).") from error
        try:
            connection = psycopg2.connect(database=secret_config.PGDATABASE, user=secret_config.PGUSER,
                                          password=secret_config.PGPASSWORD, host=secret_config.PGHOST,
                                          port=secret_config.PGPORT, connect_timeout=10)
        except AttributeError as error:
            raise Exception("secret_config.py está incompleto: debe tener PGHOST, PGDATABASE, "
                            "PGUSER, PGPASSWORD y PGPORT.") from error
        except psycopg2.OperationalError as error:
            raise Exception("No se pudo conectar a la base de datos. Revise los datos de "
                            "secret_config.py y su conexión a internet.") from error
        # Todas las instrucciones se ejecutan a traves de un cursor
        return connection.cursor()
