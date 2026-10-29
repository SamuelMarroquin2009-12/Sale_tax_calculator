class ErrorCalculadora(Exception):
    """ Excepcion base de la aplicacion: todas las demas excepciones propias heredan de ella """


class ErrorValorInvalido(ErrorCalculadora):
    """ Un dato ingresado (valor, cantidad, mililitros o id) no es valido """


class ErrorCategoriaDesconocida(ErrorCalculadora):
    """ La categoria de producto indicada no existe """


class ErrorNoEncontrado(ErrorCalculadora):
    """ Una fila buscada no fue encontrada en la base de datos """


class ErrorBaseDeDatos(ErrorCalculadora):
    """ La base de datos rechazo una operacion """


class ErrorTablaNoExiste(ErrorBaseDeDatos):
    """ La tabla calculos no existe: hay que crearla primero """


class ErrorConexion(ErrorBaseDeDatos):
    """ No se pudo conectar a la base de datos """


class ErrorConfiguracion(ErrorCalculadora):
    """ Faltan los datos de conexion (secret_config.py o variables de entorno) """