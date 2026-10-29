from model.categoria import Categoria
from model.guia_impuestos import CONCEPTOS_CLAVE, GUIA


class GuiaController:
    @staticmethod
    def armar_guia() -> dict:
        impuestos = []

        for categoria in Categoria.listar():
            info = GUIA[categoria.clave]

            impuesto = categoria.calcular_impuesto(
                info["ejemplo_valor"],
                info.get("ejemplo_ml", 0)
            )

            impuestos.append({
                "categoria": categoria,
                "info": info,
                "ejemplo_impuesto": impuesto
            })

        return {
            "impuestos": impuestos,
            "conceptos": CONCEPTOS_CLAVE
        }
