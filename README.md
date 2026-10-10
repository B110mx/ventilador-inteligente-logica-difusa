# Ventilador Inteligente con Lógica Difusa

## 1. Problemática a resolver
En muchos espacios cerrados (como salones de clases, oficinas o habitaciones), los ventiladores convencionales requieren un ajuste manual constante. Esto genera incomodidad térmica: cuando la temperatura baja, el ventilador puede seguir en alta velocidad, causando frío excesivo, y cuando hace calor, puede tardar en ajustarse, causando incomodidad. Esto no solo afecta el confort de los usuarios, sino que también ocasiona un consumo de energía ineficiente.

## 2. Descripción del proyecto
El "Ventilador Inteligente" es un prototipo de software desarrollado en Python que recomienda la velocidad de ventilación para un salón en función de la temperatura ambiente utilizando **lógica difusa**. No controla hardware: el usuario puede ingresar la temperatura o consultar automáticamente la temperatura exterior mediante Open-Meteo. El sistema calcula una recomendación teórica y muestra un medidor y gráficas del proceso.

## 3. Rama de IA
Este proyecto se enmarca dentro de la **Inteligencia Artificial Simbólica / Clásica**, específicamente en el campo de los **Sistemas Expertos** mediante el uso de **Lógica Difusa (Fuzzy Logic)**. A diferencia de la lógica booleana estricta (verdadero/falso), la lógica difusa permite manejar grados de verdad (por ejemplo, "qué tan frío o caliente" está el salón), imitando el razonamiento humano para tomar decisiones más precisas.

## 4. Caso de uso
**Actor principal:** Usuario (ej. Profesor o alumno en un salón de clases).
**Descripción:** El usuario ingresa una temperatura y humedad o consulta el clima de una ciudad. El sistema evalúa qué tan fría, templada o caliente es la temperatura, aplica un ajuste difuso según la humedad y recomienda una intensidad de ventilación. El usuario puede consultar las gráficas, el historial y el simulador para comprender la decisión.

## 5. Requisitos
- **Sistema Operativo:** Windows, macOS o Linux.
- **Lenguaje:** Python 3.10 o superior.
- **Dependencias:** `tkinter` (incluido en Python estándar) y `matplotlib`.
- **Modo automático:** conexión a internet para consultar Open-Meteo; no requiere clave de API.
- **Rango de temperatura:** de 10 °C a 40 °C.
- Las dependencias externas están detalladas en `requirements.txt`.

## 6. Instrucciones de instalación y ejecución (Local)
1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/B110mx/ventilador-inteligente-logica-difusa.git
   cd ventilador-inteligente-logica-difusa
   ```
2. **Crear y activar un entorno virtual (Opcional pero recomendado):**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```
3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Ejecutar el programa principal:**
   ```bash
   python main.py
   ```

## 7. Versión web

El sistema también puede utilizarse directamente desde el navegador, sin instalar Python:

**[Abrir Ventilador Inteligente Web](https://b110mx.github.io/ventilador-inteligente-logica-difusa/)**

La versión web conserva la validación de temperatura, el cálculo de lógica difusa, el medidor de velocidad y las gráficas de pertenencia, activación y respuesta.

La pestaña **Simulador práctico** representa un salón y anima un ventilador según el porcentaje calculado. La velocidad de las aspas, el flujo de aire, el estado y la explicación se actualizan con la misma salida del motor difuso; no existe un cálculo independiente para la animación.

La versión 1.4 incorpora humedad relativa como segunda entrada, funciones de pertenencia con transiciones graduales, búsqueda de ciudad mediante la API geográfica de Open-Meteo y un historial temporal de las últimas ocho decisiones. La humedad seca puede reducir ligeramente la recomendación y la humedad elevada puede aumentarla.

### Modo automático con datos meteorológicos

El botón **Usar temperatura actual** solicita la ubicación del navegador y consulta Open-Meteo. Si el permiso de ubicación no está disponible, utiliza Tehuacán, Puebla como ubicación predeterminada. La opción de actualización automática repite la consulta cada 10 minutos. La temperatura exterior se valida antes de enviarse a `fuzzy_logic.py`; si la API falla, el usuario puede continuar con la entrada manual. La API aporta el dato y la lógica difusa sigue tomando la decisión.

### Reglas de recomendación

- Fría: pertenencia máxima hasta 18 °C y transición gradual hasta 24 °C.
- Templada: función triangular entre 18 °C y 34 °C, con máximo a 26 °C.
- Caliente: comienza a activarse a 28 °C y alcanza su máximo a 36 °C.
- Humedad seca: puede reducir hasta 5 puntos la recomendación.
- Humedad alta: puede aumentar hasta 10 puntos la recomendación.

## 8. Créditos y licencias
- **Desarrollo:** Realizado por el equipo integrado por Abril Miranda, Mariana Córdova, Luis Bryan, Francesco Romero y Josué David.
- **Librerías:** 
  - [Tkinter](https://docs.python.org/3/library/tkinter.html) (Licencia Python)
  - [Matplotlib](https://matplotlib.org/) (Licencia PSF)
- **Uso de Inteligencia Artificial:** 
  - La estructura y refactorización de código base, además de la integración del archivo `main.py`, la optimización del archivo `interface.py` y la estructuración final del `README.md` contaron con la asistencia de Modelos de Lenguaje Grandes (LLMs).
  - Los scripts de evaluación y componentes iniciales de lógica matemática fueron creados y modificados manualmente por el equipo.

## 9. Bitácora de prompts
A continuación, algunos de los prompts clave utilizados para ayudar en la generación del código y estructuración:
1. *"Crea una estructura base en Python para evaluar funciones de pertenencia de temperatura (frío, templado, caliente)."*
2. *"Necesito un script de validación robusto en Python que compruebe que la entrada de temperatura esté entre 10 y 40 grados Celsius."*
3. *"Genera una interfaz en Tkinter con un diseño moderno, tipo tarjeta (card), y un canvas con un medidor semicircular (gauge) dinámico."*
4. *"Crea gráficos de Matplotlib para visualizar la pertenencia, activación de reglas y la curva de respuesta para un sistema de lógica difusa."*
5. *"Escribe un README.md estructurado para la entrega del proyecto de IA, incluyendo la problemática, descripción, instrucciones y uso de IA."*
