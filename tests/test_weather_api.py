"""Pruebas de la lectura meteorológica sin realizar solicitudes reales."""

import io
import sys
import unittest
from pathlib import Path


SRC_DIRECTORY = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SRC_DIRECTORY))

from weather_api import WeatherAPIError, get_current_temperature  # noqa: E402


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *_args):
        self.close()


class WeatherAPITests(unittest.TestCase):
    def test_returns_structured_temperature(self):
        def opener(_url, timeout):
            self.assertEqual(timeout, 3)
            return FakeResponse(b'{"current":{"temperature_2m":27.4,"time":"2026-10-09T12:00"}}')

        reading = get_current_temperature(timeout=3, opener=opener)
        self.assertEqual(reading.temperature, 27.4)
        self.assertEqual(reading.observed_at, "2026-10-09T12:00")
        self.assertEqual(reading.location, "Tehuacán, Puebla")

    def test_reports_invalid_api_response(self):
        def opener(_url, timeout):
            return FakeResponse(b'{"current":{}}')

        with self.assertRaises(WeatherAPIError):
            get_current_temperature(opener=opener)


if __name__ == "__main__":
    unittest.main()
