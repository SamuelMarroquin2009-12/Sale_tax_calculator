"""Punto de entrada: conecta a la base de datos y abre la consola.

    python main.py
"""
from src.controller import controller
from src.view import consola


def main():
    motor, aviso = controller.iniciar_base_datos()
    print(f"Base de datos: {motor}")
    if aviso:
        print(f"Aviso: {aviso}")
    try:
        consola.ejecutar()
    finally:
        controller.cerrar_base_datos()


if __name__ == "__main__":
    main()
