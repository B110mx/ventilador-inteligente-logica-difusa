"""Pruebas de las funciones de entrada y validación de temperatura."""

import math
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIRECTORY = PROJECT_ROOT / "src"
if str(SRC_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SRC_DIRECTORY))

from data_validation import (  # noqa: E402
    MAX_TEMPERATURE_C,
    MIN_TEMPERATURE_C,
    TemperatureValidationError,
    is_valid_temperature,
    parse_temperature,
    parse_humidity,
)


class ParseTemperatureTests(unittest.TestCase):
    """Comprueba entradas válidas, límites y datos incorrectos."""

    def test_accepts_integer_and_decimal_numbers(self):
        cases = [(25, 25.0), (22.5, 22.5), (10, 10.0)]
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(parse_temperature(value), expected)

    def test_accepts_trimmed_text_and_decimal_comma(self):
        cases = [(" 24 ", 24.0), ("25.5", 25.5), ("18,75", 18.75)]
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(parse_temperature(value), expected)

    def test_accepts_both_range_limits(self):
        self.assertEqual(parse_temperature(MIN_TEMPERATURE_C), 10.0)
        self.assertEqual(parse_temperature(MAX_TEMPERATURE_C), 40.0)

    def test_rejects_empty_and_non_numeric_text(self):
        for value in ("", "   ", "caliente", "20 grados"):
            with self.subTest(value=value):
                with self.assertRaises(TemperatureValidationError):
                    parse_temperature(value)

    def test_rejects_values_outside_the_allowed_range(self):
        for value in (9.9, 40.1, "-20", "100"):
            with self.subTest(value=value):
                with self.assertRaises(TemperatureValidationError):
                    parse_temperature(value)

    def test_rejects_non_finite_numbers(self):
        for value in (math.nan, math.inf, -math.inf, "NaN", "Infinity"):
            with self.subTest(value=value):
                with self.assertRaises(TemperatureValidationError):
                    parse_temperature(value)

    def test_rejects_boolean_and_unsupported_types(self):
        for value in (True, False, None, [], {}):
            with self.subTest(value=value):
                with self.assertRaises(TemperatureValidationError):
                    parse_temperature(value)


class IsValidTemperatureTests(unittest.TestCase):
    """Comprueba la función auxiliar de validación booleana."""

    def test_reports_valid_and_invalid_inputs(self):
        self.assertTrue(is_valid_temperature("28,5"))
        self.assertFalse(is_valid_temperature("sin dato"))
        self.assertFalse(is_valid_temperature(75))


class ParseHumidityTests(unittest.TestCase):
    def test_accepts_humidity_range(self):
        self.assertEqual(parse_humidity("55,5"), 55.5)
        self.assertEqual(parse_humidity(0), 0.0)
        self.assertEqual(parse_humidity(100), 100.0)

    def test_rejects_invalid_humidity(self):
        for value in ("", "alta", -1, 101, math.inf):
            with self.subTest(value=value):
                with self.assertRaises(TemperatureValidationError):
                    parse_humidity(value)


if __name__ == "__main__":
    unittest.main()

