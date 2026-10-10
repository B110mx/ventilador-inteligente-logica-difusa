"""Gráficas de la recomendación de ventilación con lógica difusa.

Usa las funciones de pertenencia y el cálculo de recomendación de fuzzy_logic.py,
así que las gráficas siempre coinciden con lo que calcula el sistema.

Funciones (todas devuelven un matplotlib.figure.Figure):
    grafica_pertenencia(temperatura=None)   Fría / Templado / Caliente
    grafica_activacion(temperatura)         grado de activación de cada regla
    grafica_respuesta(temperatura=None)     curva temperatura -> recomendación
    embed_figure(fig, parent)               muestra una figura dentro de Tkinter

Prueba independiente:  python src/visualization.py
"""

from matplotlib.figure import Figure

from fuzzy_logic import (
    calcular_velocidad,
    pertenencia_caliente,
    pertenencia_fria,
    pertenencia_templado,
)

TEMP_MIN = 10
TEMP_MAX = 40

COLOR_FRIA = "#2E86DE"
COLOR_TEMPLADO = "#10AC84"
COLOR_CALIENTE = "#EE5253"
COLOR_VELOCIDAD = "#8E44AD"

CONJUNTOS = [
    ("Fría", pertenencia_fria, COLOR_FRIA),
    ("Templado", pertenencia_templado, COLOR_TEMPLADO),
    ("Caliente", pertenencia_caliente, COLOR_CALIENTE),
]


def _rango(paso=0.5):
    n = int((TEMP_MAX - TEMP_MIN) / paso)
    return [TEMP_MIN + i * paso for i in range(n + 1)]


def _nueva_figura(fig):
    fig = fig or Figure(figsize=(6, 3.6), dpi=100)
    fig.clear()
    return fig, fig.add_subplot(111)


def grafica_pertenencia(temperatura=None, fig=None):
    """Funciones de pertenencia; si se da temperatura, marca el punto de entrada."""
    fig, ax = _nueva_figura(fig)
    xs = _rango()

    for nombre, funcion, color in CONJUNTOS:
        ys = [funcion(x) for x in xs]
        ax.plot(xs, ys, label=nombre, color=color, linewidth=2)
        ax.fill_between(xs, ys, alpha=0.12, color=color)
        if temperatura is not None:
            grado = funcion(temperatura)
            if grado > 0:
                ax.plot(temperatura, grado, "o", color=color)

    if temperatura is not None:
        ax.axvline(temperatura, color="black", linestyle="--", linewidth=1.2)

    ax.set_title(
        "Funciones de pertenencia"
        + (f" (entrada = {temperatura:g} °C)" if temperatura is not None else "")
    )
    ax.set_xlabel("Temperatura (°C)")
    ax.set_ylabel("Grado de pertenencia")
    ax.set_ylim(-0.02, 1.05)
    ax.grid(alpha=0.3)
    ax.legend(loc="center left")
    fig.tight_layout()
    return fig


def grafica_activacion(temperatura, fig=None):
    """Barras con el grado de activación de cada regla para la temperatura dada."""
    fig, ax = _nueva_figura(fig)
    velocidad, fria, templado, caliente = calcular_velocidad(temperatura)

    nombres = ["Fría\n(→ 0%)", "Templado\n(→ 50%)", "Caliente\n(→ 100%)"]
    grados = [fria, templado, caliente]
    colores = [COLOR_FRIA, COLOR_TEMPLADO, COLOR_CALIENTE]

    barras = ax.bar(nombres, grados, color=colores)
    for barra, grado in zip(barras, grados):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            grado + 0.02,
            f"{grado:.2f}",
            ha="center",
            fontweight="bold",
        )

    ax.set_title(
        f"Activación de reglas a {temperatura:g} °C " f"→ ventilación {velocidad:.1f}%"
    )
    ax.set_ylabel("Grado de activación")
    ax.set_ylim(0, 1.15)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    return fig


def grafica_respuesta(temperatura=None, fig=None):
    """Curva temperatura -> recomendación; marca el punto actual si se proporciona."""
    fig, ax = _nueva_figura(fig)
    xs = _rango()
    ys = [calcular_velocidad(x)[0] for x in xs]
    ax.plot(xs, ys, color=COLOR_VELOCIDAD, linewidth=2.2)

    if temperatura is not None:
        velocidad = calcular_velocidad(temperatura)[0]
        ax.plot(
            temperatura,
            velocidad,
            "o",
            color="black",
            markersize=9,
            label=f"{temperatura:g} °C → {velocidad:.1f}%",
        )
        ax.legend(loc="lower right")

    ax.set_title("Respuesta del sistema difuso")
    ax.set_xlabel("Temperatura (°C)")
    ax.set_ylabel("Ventilación recomendada (%)")
    ax.set_ylim(0, 105)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def embed_figure(fig, parent):
    """Inserta una figura en un Frame/Toplevel de Tkinter y devuelve el canvas.

    Para actualizar: volver a llamar a la grafica con fig=fig y luego canvas.draw().
    """
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    return canvas


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    t = 26.0
    grafica_pertenencia(t, fig=plt.figure(1))
    grafica_activacion(t, fig=plt.figure(2))
    grafica_respuesta(t, fig=plt.figure(3))
    plt.show()
