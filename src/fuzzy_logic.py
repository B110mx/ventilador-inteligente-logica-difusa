"""Sistema difuso para controlar la velocidad de un ventilador.

Este programa recibe la temperatura ambiente y la evalua con tres
reglas difusas principales:
- temperatura baja: velocidad baja
- temperatura templada: velocidad media
- temperatura caliente: velocidad rapida

La idea es usar grados de pertenencia para representar que tan fuerte
se ajusta cada regla a la temperatura ingresada, y luego combinar esos
valores para obtener una velocidad recomendada.
"""


def pertenencia_fria(temperatura):
    """Devuelve el grado de pertenencia de la temperatura a la zona fria/baja.

    Entre 18°C y 24°C la pertenencia disminuye de 1.0 a 0.0.
    """
    if temperatura <= 18:
        return 1.0
    elif temperatura >= 24:
        return 0.0
    return (24 - temperatura) / 6


def pertenencia_templado(temperatura):
    """Determina que tan templada es la temperatura.

    Si la temperatura está entre 21°C y 28°C, se calcula una
    pertenencia intermedia que crece y luego decrece.
    """
    if temperatura <= 21:
        return 0.0
    elif temperatura >= 28:
        return 0.0
    if temperatura <= 24:
        return (temperatura - 21) / 3
    return (28 - temperatura) / 4


def pertenencia_caliente(temperatura):
    """Calcula el grado de pertenencia a la zona de temperatura caliente.

    A partir de 25°C la temperatura empieza a aumentar su pertenencia,
    llegando a 1.0 cuando se acerca a 35°C o más.
    """
    if temperatura <= 25:
        return 0.0
    elif temperatura >= 35:
        return 1.0
    return (temperatura - 25) / 10


def calcular_velocidad(temperatura):
    """Combina las reglas difusas para obtener un valor final de velocidad.

    Args:
        temperatura (float): Valor de la temperatura ingresada en grados Celsius.

    Returns:
        tuple: (velocidad, fria, templado, caliente)
    """
    fria = pertenencia_fria(temperatura)
    templado = pertenencia_templado(temperatura)
    caliente = pertenencia_caliente(temperatura)

    suma = fria + templado + caliente
    if suma == 0:
        return 0.0, fria, templado, caliente

    velocidad = (
        fria * 33 + templado * 66 + caliente * 100
    ) / suma

    return velocidad, fria, templado, caliente


def nivel_temperatura(temperatura):
    """Clasifica la temperatura en una etiqueta general del sistema.

    Devuelve:
        "Fria" para temperaturas bajas,
        "Templado" para valores medios,
        "Caliente" para valores altos.
    """
    if temperatura < 21:
        return "Fria"
    elif temperatura <= 28:
        return "Templado"
    return "Caliente"


def nivel_velocidad(temperatura):
    """Asigna la velocidad recomendada segun el rango de temperatura."""
    if temperatura < 21:
        return "Baja"
    elif temperatura <= 28:
        return "Media"
    return "Rapida"


def mostrar_resultado(temperatura):
    """Imprime el resultado final del sistema para una temperatura dada."""
    velocidad, fria, templado, caliente = calcular_velocidad(temperatura)
    temperatura_nivel = nivel_temperatura(temperatura)
    velocidad_nivel = nivel_velocidad(temperatura)
    print("\n--- Resultado ---")
    print(f"Temperatura ingresada: {temperatura:.1f} °C ({temperatura_nivel})")
    print(f"Velocidad recomendada del ventilador: {velocidad:.1f}% ({velocidad_nivel})")


def pedir_temperatura():
    """Pide la temperatura al usuario y valida que sea un valor aceptable."""
    while True:
        entrada = input("Ingrese la temperatura del salon (°C): ").strip()
        try:
            temperatura = float(entrada.replace(",", "."))
            if temperatura < 10 or temperatura > 40:
                print("Error: la temperatura debe estar entre 10 y 40 °C.")
                continue
            return temperatura
        except ValueError:
            print("Error: debe ingresar un numero valido.")


def main():
    """Menu principal del programa.

    Permite ingresar una temperatura o salir del sistema.
    """
    while True:
        print("===========================================")
        print(" SISTEMA DIFUSO - CONTROL DE VENTILADOR")
        print("===========================================")
        print("1. Ingresar temperatura")
        print("2. Salir")

        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            temperatura = pedir_temperatura()
            mostrar_resultado(temperatura)
        elif opcion == "2":
            print("Hasta luego.")
            break
        else:
            print("Opcion no valida. Intente de nuevo.")
            print()


if __name__ == "__main__":
    main()
