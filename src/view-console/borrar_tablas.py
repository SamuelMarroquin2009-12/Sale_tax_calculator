import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from controller.calculos_controller import CalculosController

try:
    confirmacion = input("Se borrarán todos los cálculos guardados. Escriba SI para continuar: ")
    if confirmacion.strip().upper() == "SI":
        CalculosController.borrar_tabla()
        print("Tabla calculos borrada correctamente!")
    else:
        print("No se borró nada.")
except Exception as err:
    print("Error:")
    print(str(err))
