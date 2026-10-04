# Ventilador Inteligente con Lógica Difusa

## 1. Problemática a resolver
En muchos espacios cerrados (como salones de clases, oficinas o habitaciones), los ventiladores convencionales requieren un ajuste manual constante. Esto genera incomodidad térmica: cuando la temperatura baja, el ventilador puede seguir en alta velocidad, causando frío excesivo, y cuando hace calor, puede tardar en ajustarse, causando incomodidad. Esto no solo afecta el confort de los usuarios, sino que también ocasiona un consumo de energía ineficiente.

## 2. Descripción del proyecto
El "Ventilador Inteligente" es un prototipo de software desarrollado en Python que automatiza la regulación de la velocidad de un ventilador en función de la temperatura ambiente utilizando **lógica difusa**. Cuenta con una interfaz gráfica amigable donde el usuario ingresa la temperatura, y el sistema calcula en tiempo real (mostrando gráficas del proceso) el porcentaje exacto de velocidad que debería tener el ventilador.

## 3. Rama de IA
Este proyecto se enmarca dentro de la **Inteligencia Artificial Simbólica / Clásica**, específicamente en el campo de los **Sistemas Expertos** mediante el uso de **Lógica Difusa (Fuzzy Logic)**. A diferencia de la lógica booleana estricta (verdadero/falso), la lógica difusa permite manejar grados de verdad (por ejemplo, "qué tan frío o caliente" está el salón), imitando el razonamiento humano para tomar decisiones más precisas.

## 4. Caso de uso
**Actor principal:** Usuario (ej. Profesor o alumno en un salón de clases).
**Descripción:** El usuario interactúa con la interfaz gráfica ingresando la lectura actual del termómetro del salón (ej. 24.5 °C). El sistema recibe este dato, lo pasa por un proceso de *fuzzificación* (evaluando qué tan "Fría", "Templada" o "Caliente" es la temperatura), aplica las reglas de inferencia y finalmente *defuzzifica* el resultado para devolver una velocidad específica (ej. 60.5% de velocidad). El usuario también puede ver las gráficas de pertenencia y activación de reglas para comprender la decisión del sistema.

## 5. Requisitos
- **Sistema Operativo:** Windows, macOS o Linux.
- **Lenguaje:** Python 3.8 o superior.
- **Dependencias:** `tkinter` (incluido en Python estándar) y `matplotlib`.
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

## 7. Créditos y licencias
- **Desarrollo:** Realizado por el equipo integrado por Abril Miranda, Mariana Córdova, Luis Bryan, Francesco Romero y Josué David.
- **Librerías:** 
  - [Tkinter](https://docs.python.org/3/library/tkinter.html) (Licencia Python)
  - [Matplotlib](https://matplotlib.org/) (Licencia PSF)
- **Uso de Inteligencia Artificial:** 
  - La estructura y refactorización de código base, además de la integración del archivo `main.py`, la optimización del archivo `interface.py` y la estructuración final del `README.md` contaron con la asistencia de Modelos de Lenguaje Grandes (LLMs).
  - Los scripts de evaluación y componentes iniciales de lógica matemática fueron creados y modificados manualmente por el equipo.

## 8. Bitácora de prompts
A continuación, algunos de los prompts clave utilizados para ayudar en la generación del código y estructuración:
1. *"Crea una estructura base en Python para evaluar funciones de pertenencia de temperatura (frío, templado, caliente)."*
2. *"Necesito un script de validación robusto en Python que compruebe que la entrada de temperatura esté entre -10 y 60 grados Celsius."*
3. *"Genera una interfaz en Tkinter con un diseño moderno, tipo tarjeta (card), y un canvas con un medidor semicircular (gauge) dinámico."*
4. *"Crea gráficos de Matplotlib para visualizar la pertenencia, activación de reglas y la curva de respuesta para un sistema de lógica difusa."*
5. *"Escribe un README.md estructurado para la entrega del proyecto de IA, incluyendo la problemática, descripción, instrucciones y uso de IA."*
