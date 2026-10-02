import sys

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

sys.path.append("src")

from model.impuestos_logic import calcular_impuesto


class SaleTaxCalculatorApp(App):

    def build(self):

        contenedor = GridLayout(
            cols=2,
            padding=20,
            spacing=15
        )

        # -----------------------------
        # TÍTULO
        # -----------------------------

        contenedor.add_widget(
            Label(
                text="Calculadora de Impuestos",
                font_size=30
            )
        )

        contenedor.add_widget(Label(text=""))

        # -----------------------------
        # CATEGORÍA
        # -----------------------------

        contenedor.add_widget(
            Label(
                text="Categoría de la compra",
                font_size=20
            )
        )

        self.categorias = {
            "Canasta básica / Exento": "exento",
            "Alimentos con IVA 5%": "iva5",
            "Bienes generales IVA 19%": "iva19",
            "Restaurantes (INC 8%)": "inc_restaurantes",
            "Licores": "licores",
            "Bienes suntuarios": "suntuarios",
            "Bolsas plásticas": "bolsas",
            "Cigarrillos / Vapeadores": "vapeadores"
        }

        self.categoria = Spinner(
            text="Seleccione una categoría",
            values=list(self.categorias.keys()),
            font_size=18
        )

        contenedor.add_widget(self.categoria)

        # -----------------------------
        # PRECIO
        # -----------------------------

        contenedor.add_widget(
            Label(
                text="Precio unitario (COP)",
                font_size=20
            )
        )

        self.precio = TextInput(
            font_size=25,
            input_filter="int",
            multiline=False,
            hint_text="Ej: 50000"
        )

        contenedor.add_widget(self.precio)

        # -----------------------------
        # CANTIDAD
        # -----------------------------

        contenedor.add_widget(
            Label(
                text="Cantidad de unidades",
                font_size=20
            )
        )

        self.cantidad = TextInput(
            font_size=25,
            input_filter="int",
            multiline=False,
            hint_text="Ej: 2"
        )

        contenedor.add_widget(self.cantidad)

        # -----------------------------
        # BOTÓN CALCULAR
        # -----------------------------

        calcular = Button(
            text="Calcular",
            font_size=25
        )

        calcular.bind(
            on_press=self.calcular_cuota
        )

        contenedor.add_widget(calcular)

        # -----------------------------
        # BOTÓN LIMPIAR
        # -----------------------------

        limpiar = Button(
            text="Limpiar",
            font_size=25
        )

        limpiar.bind(
            on_press=self.limpiar
        )

        contenedor.add_widget(limpiar)

        # -----------------------------
        # RESULTADO
        # -----------------------------

        contenedor.add_widget(
            Label(
                text="Resultado:",
                font_size=20
            )
        )

        self.resultado = Label(
            text="Ingrese los datos y presione Calcular",
            font_size=18
        )

        contenedor.add_widget(self.resultado)

        return contenedor

    # ==========================================
    # VALIDAR DATOS
    # ==========================================

    def validar(self):

        if self.categoria.text == "Seleccione una categoría":
            raise Exception(
                "Debe seleccionar una categoría."
            )

        if not self.precio.text:
            raise Exception(
                "Debe ingresar un precio."
            )

        if not self.precio.text.isnumeric():
            raise Exception(
                "El precio debe ser un número entero positivo."
            )

        if int(self.precio.text) <= 0:
            raise Exception(
                "El precio debe ser mayor que cero."
            )

        if not self.cantidad.text:
            raise Exception(
                "Debe ingresar una cantidad."
            )

        if not self.cantidad.text.isnumeric():
            raise Exception(
                "La cantidad debe ser un número entero positivo."
            )

        if int(self.cantidad.text) <= 0:
            raise Exception(
                "La cantidad debe ser mayor que cero."
            )

    # ==========================================
    # CALCULAR
    # ==========================================

    def calcular_cuota(self, sender):

        try:

            self.validar()

            # Nombre que seleccionó el usuario
            categoria_visible = self.categoria.text

            # Clave que necesita el modelo
            categoria = self.categorias[categoria_visible]

            precio = int(self.precio.text)
            cantidad = int(self.cantidad.text)

            # Llamamos al modelo
            valor_total, impuesto = calcular_impuesto(
                categoria,
                precio,
                cantidad
            )

            total_pagar = valor_total + impuesto

            self.resultado.text = (
                f"Valor de la compra: ${valor_total:,.0f}\n"
                f"Impuesto: ${impuesto:,.0f}\n"
                f"Total a pagar: ${total_pagar:,.0f}"
            )

        except Exception as err:

            self.mostrar_error(err)

    # ==========================================
    # LIMPIAR
    # ==========================================

    def limpiar(self, sender):

        self.categoria.text = "Seleccione una categoría"

        self.precio.text = ""

        self.cantidad.text = ""

        self.resultado.text = (
            "Ingrese los datos y presione Calcular"
        )

    # ==========================================
    # MOSTRAR ERROR
    # ==========================================

    def mostrar_error(self, err):

        contenido = GridLayout(
            cols=1,
            padding=15,
            spacing=10
        )

        contenido.add_widget(
            Label(
                text=str(err),
                font_size=18
            )
        )

        cerrar = Button(
            text="Cerrar"
        )

        contenido.add_widget(cerrar)

        popup = Popup(
            title="Error",
            content=contenido,
            size_hint=(0.8, 0.4)
        )

        cerrar.bind(
            on_press=popup.dismiss
        )

        popup.open()


if __name__ == "__main__":
    SaleTaxCalculatorApp().run()
