from unittest.mock import patch

from calendario.main import main, obtener_nombre_archivo


class TestMain:

    @patch("sys.argv", ["calendario", "invalid", "01-01-2025"])
    def test_formato_fecha_invalido(self, capsys):
        main()
        captured = capsys.readouterr()
        assert "formato de fecha invalido" in captured.out

    @patch("sys.argv", ["calendario", "15-03-2025", "01-01-2025"])
    def test_inicio_mayor_que_fin(self, capsys):
        main()
        captured = capsys.readouterr()
        assert "fecha de inicio no puede ser mayor" in captured.out


class TestObtenerNombreArchivo:

    @patch("os.path.exists", return_value=False)
    def test_primer_archivo(self, mock_exists):
        resultado = obtener_nombre_archivo()
        assert resultado == "calendario-01.pdf"

    @patch("os.path.exists", side_effect=[True, True, False])
    def test_tercer_archivo(self, mock_exists):
        resultado = obtener_nombre_archivo()
        assert resultado == "calendario-03.pdf"
