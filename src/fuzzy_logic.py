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

    La regla permanece activa por debajo de 20 °C y recomienda apagar
    el ventilador. Al llegar a 20 °C comienza la ventilación inicial.
    """
    return 1.0 if temperatura < 20 else 0.0


def pertenencia_templado(temperatura):
    """Determina la activación de la regla de ventilación inicial.

    La pertenencia vale 1.0 a 20 °C y desciende gradualmente hasta
    llegar a 0.0 a 40 °C.
    """
    if temperatura < 20 or temperatura >= 40:
        return 0.0
    return (40 - temperatura) / 20


def pertenencia_caliente(temperatura):
    """Calcula la activación de la regla de ventilación máxima.

    Comienza en 0.0 a 20 °C y aumenta de forma lineal hasta 1.0
    a 40 °C.
    """
    if temperatura <= 20:
        return 0.0
    if temperatura >= 40:
        return 1.0
    return (temperatura - 20) / 20


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

    # Consecuentes de las reglas: apagado, ventilación inicial y máxima.
    velocidad = (fria * 0 + templado * 25 + caliente * 100) / suma

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
