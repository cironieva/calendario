from datetime import datetime

from calendario.fechas import calcular_semanas, formatear_fecha


class TestCalcularSemanas:

    def test_inicio_lunes_fin_domingo(self):
        """Cuando inicio es lunes y fin es domingo, los limites no cambian."""
        inicio = datetime(2025, 1, 6)   # lunes
        fin = datetime(2025, 1, 12)     # domingo
        start_monday, end_sunday, num_weeks = calcular_semanas(inicio, fin)
        assert start_monday == inicio
        assert end_sunday == fin
        assert num_weeks == 1

    def test_inicio_miercoles(self):
        """Si inicio cae miercoles, retrocede al lunes anterior."""
        inicio = datetime(2025, 1, 8)   # miercoles
        fin = datetime(2025, 1, 12)     # domingo
        start_monday, end_sunday, num_weeks = calcular_semanas(inicio, fin)
        assert start_monday == datetime(2025, 1, 6)   # lunes anterior
        assert end_sunday == datetime(2025, 1, 12)
        assert num_weeks == 1

    def test_fin_jueves(self):
        """Si fin cae jueves, avanza al domingo siguiente."""
        inicio = datetime(2025, 1, 6)   # lunes
        fin = datetime(2025, 1, 9)      # jueves
        start_monday, end_sunday, num_weeks = calcular_semanas(inicio, fin)
        assert start_monday == datetime(2025, 1, 6)
        assert end_sunday == datetime(2025, 1, 12)    # domingo siguiente
        assert num_weeks == 1

    def test_varias_semanas(self):
        """Rango que abarca varias semanas."""
        inicio = datetime(2025, 1, 6)   # lunes
        fin = datetime(2025, 1, 26)     # domingo
        start_monday, end_sunday, num_weeks = calcular_semanas(inicio, fin)
        assert num_weeks == 3

    def test_mismo_dia(self):
        """Inicio y fin en el mismo dia expande a semana completa."""
        inicio = datetime(2025, 1, 8)   # miercoles
        fin = datetime(2025, 1, 8)
        start_monday, end_sunday, num_weeks = calcular_semanas(inicio, fin)
        assert start_monday == datetime(2025, 1, 6)
        assert end_sunday == datetime(2025, 1, 12)
        assert num_weeks == 1


class TestFormatearFecha:

    def test_primer_dia_del_calendario(self):
        """El primer dia del calendario muestra formato completo."""
        inicio = datetime(2025, 3, 15)
        resultado = formatear_fecha(inicio, inicio)
        assert resultado == "15 de marzo"

    def test_primero_de_mes(self):
        """El dia 1 de cualquier mes muestra formato completo."""
        fecha = datetime(2025, 4, 1)
        inicio = datetime(2025, 3, 15)
        resultado = formatear_fecha(fecha, inicio)
        assert resultado == "1 de abril"

    def test_dia_normal(self):
        """Un dia cualquiera muestra solo el numero."""
        fecha = datetime(2025, 3, 20)
        inicio = datetime(2025, 3, 15)
        resultado = formatear_fecha(fecha, inicio)
        assert resultado == "20"

    def test_primero_de_enero(self):
        """El 1 de enero muestra formato completo (es dia 1)."""
        fecha = datetime(2025, 1, 1)
        inicio = datetime(2024, 12, 1)
        resultado = formatear_fecha(fecha, inicio)
        assert resultado == "1 de enero"

    def test_ultimo_mes(self):
        """Diciembre funciona correctamente."""
        fecha = datetime(2025, 12, 15)
        inicio = datetime(2025, 12, 1)
        resultado = formatear_fecha(fecha, inicio)
        assert resultado == "15"
