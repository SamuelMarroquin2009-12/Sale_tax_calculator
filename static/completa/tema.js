/* Modo claro / oscuro: aplica el tema guardado (o el del sistema) y maneja el boton de cambio */
(function () {
  var tema = null;
  try { tema = localStorage.getItem("tema"); } catch (e) {}
  if (!tema) { tema = window.matchMedia("(prefers-color-scheme: dark)").matches ? "oscuro" : "claro"; }
  document.documentElement.setAttribute("data-tema", tema);  /* antes de pintar: evita parpadeos */

  document.addEventListener("DOMContentLoaded", function () {
    var boton = document.getElementById("boton-tema");
    if (!boton) { return; }
    boton.addEventListener("click", function () {
      var nuevo = document.documentElement.getAttribute("data-tema") === "oscuro" ? "claro" : "oscuro";
      document.documentElement.setAttribute("data-tema", nuevo);
      try { localStorage.setItem("tema", nuevo); } catch (e) {}
    });
  });
})();