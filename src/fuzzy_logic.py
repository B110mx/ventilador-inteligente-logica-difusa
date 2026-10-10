"""Sistema difuso para recomendar la velocidad de ventilación de un salón.

Este programa recibe la temperatura ambiente y la evalua con tres
reglas difusas principales:
- temperatura fría: ventilador apagado
- temperatura templada: ventilación inicial
- temperatura caliente: velocidad rapida

La idea es usar grados de pertenencia para representar que tan fuerte
se ajusta cada regla a la temperatura ingresada, y luego combinar esos
valores para obtener una velocidad recomendada.
"""


def pertenencia_fria(temperatura):
    """Devuelve el grado de pertenencia a la regla de temperatura fría.

    Permanece totalmente activa hasta 18 °C y desciende de forma gradual
    hasta desaparecer a 24 °C.
    """
    if temperatura <= 18:
        return 1.0
    if temperatura >= 24:
        return 0.0
    return (24 - temperatura) / 6


def pertenencia_templado(temperatura):
    """Determina la activación de la regla de ventilación inicial.

    Aumenta entre 18 y 26 °C y disminuye entre 26 y 34 °C.
    """
    if temperatura <= 18 or temperatura >= 34:
        return 0.0
    if temperatura <= 26:
        return (temperatura - 18) / 8
    return (34 - temperatura) / 8


def pertenencia_caliente(temperatura):
    """Calcula la activación de la regla de ventilación máxima.

    Comienza a activarse a 28 °C y alcanza su máximo a 36 °C.
    """
    if temperatura <= 28:
        return 0.0
    if temperatura >= 36:
        return 1.0
    return (temperatura - 28) / 8


def pertenencia_seca(humedad):
    if humedad <= 30:
        return 1.0
    if humedad >= 50:
        return 0.0
    return (50 - humedad) / 20


def pertenencia_humedad_comoda(humedad):
    if humedad <= 30 or humedad >= 70:
        return 0.0
    if humedad <= 50:
        return (humedad - 30) / 20
    return (70 - humedad) / 20


def pertenencia_humeda(humedad):
    if humedad <= 50:
        return 0.0
    if humedad >= 70:
        return 1.0
    return (humedad - 50) / 20


def calcular_velocidad(temperatura, humedad=50.0):
    """Combina las reglas difusas para obtener un valor final de velocidad.

    Args:
        temperatura (float): Valor de la temperatura en grados Celsius.
        humedad (float): Humedad relativa de 0 a 100 %. Su valor neutral es 50 %.

    Returns:
        tuple: (velocidad, fria, templado, caliente)
    """
    fria = pertenencia_fria(temperatura)
    templado = pertenencia_templado(temperatura)
    caliente = pertenencia_caliente(temperatura)

    suma = fria + templado + caliente
    if suma == 0:
        return 0.0, fria, templado, caliente

    # Reglas de temperatura con consecuentes tipo Sugeno: 0, 50 y 100 %.
    velocidad_base = (fria * 0 + templado * 50 + caliente * 100) / suma

    seca = pertenencia_seca(humedad)
    comoda = pertenencia_humedad_comoda(humedad)
    humeda = pertenencia_humeda(humedad)
    suma_humedad = seca + comoda + humeda
    ajuste = 0.0
    if suma_humedad:
        # El aire seco reduce levemente y el húmedo aumenta la recomendación.
        ajuste = (seca * -5 + comoda * 0 + humeda * 10) / suma_humedad

    velocidad = min(100.0, max(0.0, velocidad_base + ajuste))

    return velocidad, fria, templado, caliente


def nivel_temperatura(temperatura):
    """Clasifica la temperatura en una etiqueta general del sistema.

    Devuelve:
        "Fria" para temperaturas bajas,
        "Templado" para valores medios,
        "Caliente" para valores altos.
    """
    if temperatura < 20:
        return "Fria"
    elif temperatura <= 30:
        return "Templado"
    return "Caliente"


def nivel_velocidad(temperatura):
    """Asigna la velocidad recomendada segun el rango de temperatura."""
    if temperatura < 20:
        return "Apagada"
    elif temperatura < 30:
        return "Baja"
    elif temperatura < 35:
        return "Media"
    return "Alta"


def mostrar_resultado(temperatura):
    """Imprime el resultado final del sistema para una temperatura dada."""
    velocidad, fria, templado, caliente = calcular_velocidad(temperatura)
    temperatura_nivel = nivel_temperatura(temperatura)
    velocidad_nivel = nivel_velocidad(temperatura)
    print("\n--- Resultado ---")
    print(f"Temperatura ingresada: {temperatura:.1f} °C ({temperatura_nivel})")
    print(f"Ventilación recomendada para el salón: {velocidad:.1f}% ({velocidad_nivel})")


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
