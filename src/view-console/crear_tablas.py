import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from controller.calculos_controller import CalculosController

try:
    CalculosController.crear_tabla()
    print("Tabla calculos creada correctamente!")
except Exception as err:
    print("Error:")
    print(str(err))
