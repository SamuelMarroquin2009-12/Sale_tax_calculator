/* Formulario de calcular: cambia las etiquetas, muestra los mililitros y la ayuda segun el impuesto elegido */
(function () {
  var radios = document.querySelectorAll('#form-calculo input[name="categoria"]'),
      campoMl = document.getElementById("campo-ml"), etiqueta = document.getElementById("etiqueta-valor"),
      signo = document.getElementById("signo"), ayuda = document.getElementById("ayuda-categoria");

  function actualizar() {
    var marcada = document.querySelector('#form-calculo input[name="categoria"]:checked');
    campoMl.style.display = marcada && marcada.dataset.ml === "si" ? "block" : "none";
    etiqueta.textContent = marcada ? marcada.dataset.etiqueta : "Valor de la compra (COP)";
    signo.style.visibility = marcada && marcada.value === "bolsas" ? "hidden" : "visible";
    if (marcada) {
      ayuda.hidden = false;
      ayuda.innerHTML = "";
      ayuda.append(marcada.dataset.resumen + " ");
      var enlace = document.createElement("a");
      enlace.href = marcada.dataset.guia;
      enlace.textContent = "Saber más";
      ayuda.append(enlace);
    }
  }

  radios.forEach(function (radio) { radio.addEventListener("change", actualizar); });
  actualizar();
})();