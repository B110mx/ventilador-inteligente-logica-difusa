"""Consulta de temperatura exterior para el modo automático.

Open-Meteo no requiere una clave de API. Este módulo solamente obtiene la
medición; la decisión de ventilación continúa a cargo de ``fuzzy_logic``.
"""

import json
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urlencode
from urllib.request import urlopen


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
DEFAULT_LATITUDE = 18.4615
DEFAULT_LONGITUDE = -97.3928
DEFAULT_LOCATION = "Tehuacán, Puebla"


class WeatherAPIError(RuntimeError):
    """Indica que no fue posible obtener una lectura meteorológica válida."""


@dataclass(frozen=True)
class WeatherReading:
    temperature: float
    observed_at: str
    location: str


def get_current_temperature(
    latitude=DEFAULT_LATITUDE,
    longitude=DEFAULT_LONGITUDE,
    location=DEFAULT_LOCATION,
    timeout=10,
    opener=urlopen,
):
    """Devuelve la temperatura exterior actual informada por Open-Meteo."""
    query = urlencode(
        {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m",
            "timezone": "auto",
        }
    )
    try:
        with opener(f"{OPEN_METEO_URL}?{query}", timeout=timeout) as response:
            payload = json.load(response)
        current = payload["current"]
        temperature = float(current["temperature_2m"])
        observed_at = current.get("time") or datetime.now().isoformat(timespec="minutes")
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        raise WeatherAPIError(
            "No fue posible consultar la temperatura. Revise la conexión o use el modo manual."
        ) from exc

    return WeatherReading(temperature, observed_at, location)
