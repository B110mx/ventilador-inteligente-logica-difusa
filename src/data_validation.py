"""Funciones para convertir y validar la temperatura de entrada.

Este módulo concentra las reglas de validación para que la interfaz y el
programa principal utilicen los mismos límites y mensajes de error.
"""

import math
from numbers import Real


MIN_TEMPERATURE_C = 10.0
MAX_TEMPERATURE_C = 40.0


class TemperatureValidationError(ValueError):
    """Indica que una entrada no representa una temperatura permitida."""


def parse_temperature(value):
    """Convierte una entrada a grados Celsius y comprueba su intervalo.

    Acepta números o texto. En las cadenas se permiten tanto el punto como la
    coma decimal. El resultado siempre se devuelve como ``float``.

    Args:
        value: Número o cadena que contiene la temperatura.

    Returns:
        float: Temperatura validada en grados Celsius.

    Raises:
        TemperatureValidationError: Si la entrada está vacía, no es numérica,
            no es finita o está fuera del intervalo de 10 a 40 °C.
    """
    if isinstance(value, bool):
        raise TemperatureValidationError("La temperatura debe ser un número.")

    if isinstance(value, str):
        normalized = value.strip().replace(",", ".")
        if not normalized:
            raise TemperatureValidationError("Ingrese una temperatura.")
        try:
            temperature = float(normalized)
        except ValueError as exc:
            raise TemperatureValidationError(
                "Ingrese una temperatura numérica válida."
            ) from exc
    elif isinstance(value, Real):
        temperature = float(value)
    else:
        raise TemperatureValidationError("La temperatura debe ser un número.")

    if not math.isfinite(temperature):
        raise TemperatureValidationError("La temperatura debe ser un valor finito.")

    if temperature < MIN_TEMPERATURE_C or temperature > MAX_TEMPERATURE_C:
        raise TemperatureValidationError(
            f"La temperatura debe estar entre {MIN_TEMPERATURE_C:g} y "
            f"{MAX_TEMPERATURE_C:g} °C."
        )

    return temperature


def is_valid_temperature(value):
    """Devuelve ``True`` cuando la entrada cumple todas las validaciones."""
    try:
        parse_temperature(value)
    except TemperatureValidationError:
        return False
    return True

