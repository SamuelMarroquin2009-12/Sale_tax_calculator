"""La consola sigue funcionando."""
from src.view import consola


def _ejecutar(monkeypatch, capsys, entradas):
    iterador = iter(entradas)
    monkeypatch.setattr("builtins.input", lambda _msg="": next(iterador))
    consola.ejecutar()
    return capsys.readouterr().out


def test_consola_insertar_y_buscar(tablas, monkeypatch, capsys):
    salida = _ejecutar(monkeypatch, capsys,
                       ["3", "5", "80000", "4", "1", "0", "0"])
    assert "Impuesto: $39.200,00" in salida
    assert "Licores" in salida


def test_consola_calcular_sin_guardar(tablas, monkeypatch, capsys):
    salida = _ejecutar(monkeypatch, capsys, ["5", "3", "100000", "0"])
    assert "$19.000,00" in salida


def test_consola_error_amigable_no_se_cae(tablas, monkeypatch, capsys):
    salida = _ejecutar(monkeypatch, capsys, ["3", "3", "abc", "9", "0"])
    assert "Error: Valor: debe ser un número" in salida
    assert "Opción inválida" in salida
    assert "¡Hasta luego!" in salida
