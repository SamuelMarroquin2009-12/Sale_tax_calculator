CONCEPTOS_CLAVE = [
    (
        "¿Qué es un impuesto?",
        "Es dinero que pagamos al Estado para financiar servicios que usamos todos: salud, educación, vías y seguridad."
    ),
    (
        "IVA (impuesto al valor agregado)",
        "Se suma al precio de casi cualquier producto o servicio. La tarifa general es del 19 %, pero algunos productos pagan menos (5 %) o nada (0 %)."
    ),
    (
        "INC (impuesto nacional al consumo)",
        "Se cobra solo en sectores específicos, como los restaurantes. Se suma a la cuenta, igual que el IVA, pero con otra tarifa y otras reglas."
    ),
    (
        "¿Quién lo paga?",
        "Tú, como comprador. El negocio lo cobra en la factura y luego lo entrega al Estado."
    ),
]

GUIA = {
    "canasta": {
        "icono": "canasta",
        "tarifa": "0 %",
        "tipo": "Exento",
        "ejemplo_valor": 100000,
        "resumen": "Productos básicos que no pagan impuesto.",
        "que_es": "Son productos de primera necesidad (por ejemplo, leche, huevos o verduras frescas) que la ley libera de impuesto para que el costo de vida de las familias no suba. La lista exacta la define la ley.",
        "como": "Pagas solo el precio del producto: el impuesto es $0."
    },
    "alimentos5": {
        "icono": "alimentos",
        "tarifa": "5 %",
        "tipo": "IVA",
        "ejemplo_valor": 100000,
        "resumen": "Algunos alimentos pagan un IVA reducido.",
        "que_es": "Ciertos alimentos procesados (por ejemplo, café, azúcar o chocolate de mesa) tienen una tarifa de IVA más baja que la general. Es un punto intermedio entre pagar nada y pagar el 19 %.",
        "como": "Se suma el 5 % al valor de la compra."
    },
    "general19": {
        "icono": "bolsa_compras",
        "tarifa": "19 %",
        "tipo": "IVA",
        "ejemplo_valor": 100000,
        "resumen": "El IVA que pagan la mayoría de productos y servicios.",
        "que_es": "Es la tarifa general del IVA. Aplica a la mayoría de lo que compramos: ropa, celulares, electrodomésticos, servicios, etc.",
        "como": "Se suma el 19 % al valor de la compra."
    },
    "restaurante": {
        "icono": "cubiertos",
        "tarifa": "8 %",
        "tipo": "INC",
        "ejemplo_valor": 100000,
        "resumen": "El impuesto al consumo de restaurantes, bares y cafeterías.",
        "que_es": "Cuando consumes en un restaurante, bar o cafetería, el negocio te cobra el impuesto nacional al consumo (INC). A veces aparece en la cuenta como 'impuesto al consumo'.",
        "como": "Se suma el 8 % al valor de la cuenta."
    },
    "licores": {
        "icono": "copa",
        "tarifa": "49 %",
        "tipo": "Consumo",
        "ejemplo_valor": 100000,
        "resumen": "Un impuesto alto sobre bebidas alcohólicas.",
        "que_es": "Es un impuesto al consumo que cobran los departamentos sobre el licor. En la ley se arma con una parte porcentual y otra según el grado de alcohol; esta calculadora usa una tarifa única simplificada.",
        "como": "Se suma el 49 % al valor de la compra."
    },
    "suntuarios": {
        "icono": "gema",
        "tarifa": "19 %",
        "tipo": "IVA",
        "ejemplo_valor": 5000000,
        "resumen": "Artículos de lujo o de alto valor.",
        "que_es": "Son bienes que no son de primera necesidad y tienen un valor alto, como joyas o embarcaciones de recreo. En esta calculadora se cobran con la tarifa de 19 %.",
        "como": "Se suma el 19 % al valor de la compra."
    },
    "bolsas": {
        "icono": "hoja",
        "tarifa": "$73 por bolsa",
        "tipo": "Ambiental",
        "ejemplo_valor": 5,
        "resumen": "Un valor fijo por cada bolsa plástica que te entregan.",
        "que_es": "Es un impuesto ambiental: busca que usemos menos bolsas plásticas en el comercio. No depende del precio de la compra, sino de cuántas bolsas recibes. El valor por bolsa cambia con los años.",
        "como": "Se cobran $73 por cada bolsa.",
        "ejemplo_texto": "5 bolsas"
    },
    "cigarrillos": {
        "icono": "cigarrillo",
        "tarifa": "30 % + $2.000 por ml",
        "tipo": "Consumo",
        "ejemplo_valor": 15000,
        "ejemplo_ml": 10,
        "resumen": "Impuesto al consumo de cigarrillos y vapeadores.",
        "que_es": "Busca desincentivar el consumo de tabaco y vapeadores y ayudar a financiar la salud. Tiene una parte porcentual sobre el precio y, en los vapeadores, otra por cada mililitro de líquido.",
        "como": "Se cobra el 30 % del valor más $2.000 por cada mililitro de líquido.",
        "ejemplo_texto": "$15.000 y 10 ml"
    },
}
