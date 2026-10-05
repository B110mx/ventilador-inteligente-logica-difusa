"""Pruebas de integración entre validación, lógica difusa y gráficas."""

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIRECTORY = PROJECT_ROOT / "src"
if str(SRC_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SRC_DIRECTORY))

from data_validation import TemperatureValidationError, parse_temperature  # noqa: E402
from fuzzy_logic import calcular_velocidad  # noqa: E402


class ValidationAndFuzzyLogicTests(unittest.TestCase):
    """Comprueba el flujo que usa la interfaz para calcular una velocidad."""

    def test_valid_text_reaches_fuzzy_calculation(self):
        cases = [("10", 33.0), ("22,5", 55.0), ("25", 66.0), ("30", 100.0)]
        for raw_value, expected_speed in cases:
            with self.subTest(raw_value=raw_value):
                temperature = parse_temperature(raw_value)
                speed = calcular_velocidad(temperature)[0]
                self.assertAlmostEqual(speed, expected_speed, places=2)

    def test_invalid_text_stops_before_calculation(self):
        with self.assertRaises(TemperatureValidationError):
            parse_temperature("temperatura alta")

    def test_speed_stays_within_percentage_limits(self):
        for temperature in range(10, 41):
            with self.subTest(temperature=temperature):
                speed = calcular_velocidad(parse_temperature(temperature))[0]
                self.assertGreaterEqual(speed, 0.0)
                self.assertLessEqual(speed, 100.0)


class VisualizationTests(unittest.TestCase):
    """Comprueba que las tres gráficas se puedan construir."""

    @classmethod
    def setUpClass(cls):
        global visualization
        try:
            import visualization
        except ModuleNotFoundError as exc:
            if exc.name == "matplotlib":
                raise unittest.SkipTest(
                    "Matplotlib no está instalado; ejecute: pip install -r requirements.txt"
                ) from exc
            raise

    def test_graph_functions_create_one_axis(self):
        figures = [
            visualization.grafica_pertenencia(22.5),
            visualization.grafica_activacion(22.5),
            visualization.grafica_respuesta(22.5),
        ]
        for figure in figures:
            with self.subTest(title=figure.axes[0].get_title()):
                self.assertEqual(len(figure.axes), 1)


if __name__ == "__main__":
    unittest.main()
