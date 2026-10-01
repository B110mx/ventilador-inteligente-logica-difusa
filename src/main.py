# Proyecto: Sistemas difusos (logica difusa)
# Prototipo: Control de velocidad de un ventilador segun la temperatura del salon


def pertenencia_fria(temperatura):
    """Calcula que tanto pertenece una temperatura al conjunto 'fria'."""
    if temperatura <= 15:
        return 1.0
    elif temperatura >= 25:
        return 0.0
    else:
        return (25 - temperatura) / 10


def pertenencia_templada(temperatura):
    """Calcula que tanto pertenece una temperatura al conjunto 'templada'."""
    if temperatura <= 15 or temperatura >= 35:
        return 0.0
    elif temperatura == 25:
        return 1.0
    elif temperatura < 25:
        return (temperatura - 15) / 10
    else:
        return (35 - temperatura) / 10


def pertenencia_caliente(temperatura):
    """Calcula que tanto pertenece una temperatura al conjunto 'caliente'."""
    if temperatura <= 25:
        return 0.0
    elif temperatura >= 35:
        return 1.0
    else:
        return (temperatura - 25) / 10


def calcular_velocidad(temperatura):
    """Aplica reglas difusas y devuelve la velocidad recomendada del ventilador."""

    # Fuzzificacion: convertir el valor exacto en grados de pertenencia.
    fria = pertenencia_fria(temperatura)
    templada = pertenencia_templada(temperatura)
    caliente = pertenencia_caliente(temperatura)

    # Valores representativos de salida para cada regla.
    velocidad_baja = 20
    velocidad_media = 55
    velocidad_alta = 100

    suma_pertenencias = fria + templada + caliente

    # Evita division entre cero si se modifica el rango en el futuro.
    if suma_pertenencias == 0:
        return 0, fria, templada, caliente

    # Defuzzificacion: promedio ponderado.
    velocidad = (
        fria * velocidad_baja
        + templada * velocidad_media
        + caliente * velocidad_alta
    ) / suma_pertenencias

    return velocidad, fria, templada, caliente


def mostrar_resultado(temperatura):
    velocidad, fria, templada, caliente = calcular_velocidad(temperatura)

    print("\n--- Grados de pertenencia ---")
    print(f"Fria:     {fria * 100:.1f}%")
    print(f"Templada: {templada * 100:.1f}%")
    print(f"Caliente: {caliente * 100:.1f}%")

    print("\n--- Resultado ---")
    print(f"Temperatura ingresada: {temperatura:.1f} °C")
    print(f"Velocidad recomendada del ventilador: {velocidad:.1f}%")


def ejecutar_pruebas():
    temperaturas = [10, 18, 22, 25, 28, 30, 35, 40]

    print("\nPruebas del sistema difuso")
    print("Temperatura | Fria | Templada | Caliente | Velocidad")
    print("------------------------------------------------------")

    for temp in temperaturas:
        velocidad, fria, templada, caliente = calcular_velocidad(temp)
        print(
            f"{temp:10.1f} | {fria*100:5.1f}% | {templada*100:8.1f}% | "
            f"{caliente*100:8.1f}% | {velocidad:8.1f}%"
        )


def main():
    print("===========================================")
    print(" SISTEMA DIFUSO - CONTROL DE VENTILADOR")
    print("===========================================")
    print("1. Ingresar temperatura")
    print("2. Ejecutar pruebas de demostracion")

    opcion = input("\nSeleccione una opcion: ")

    if opcion == "1":
        try:
            temperatura = float(input("Ingrese la temperatura del salon (°C): "))
            mostrar_resultado(temperatura)
        except ValueError:
            print("Error: debe ingresar un numero valido.")
    elif opcion == "2":
        ejecutar_pruebas()
    else:
        print("Opcion no valida.")


if __name__ == "__main__":
    main()
