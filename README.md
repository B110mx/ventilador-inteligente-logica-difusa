# Ventilador inteligente con lógica difusa

Prototipo académico que recomienda la velocidad de un ventilador a partir de la temperatura de un salón. El sistema usa grados de pertenencia para representar los estados **frío**, **templado** y **caliente**, y calcula una salida gradual mediante un promedio ponderado.

## Rama de inteligencia artificial

El proyecto pertenece a la rama de **lógica difusa**, adecuada para trabajar con valores intermedios y decisiones graduales en lugar de clasificaciones rígidas.

## Caso de uso

Regular la velocidad de un ventilador en un salón de clases para mejorar el confort y evitar cambios bruscos de velocidad.

## Requisitos

- Python 3.10 o posterior.
- No requiere paquetes externos en la versión actual.

## Instalación y ejecución

1. Clonar o descargar este repositorio.
2. Abrir una terminal en la carpeta del proyecto.
3. Ejecutar:

```bash
python src/main.py
```

El programa permite ingresar una temperatura o ejecutar la demostración incluida.

## Datos de prueba

La demostración utiliza temperaturas de 10, 18, 22, 25, 28, 30, 35 y 40 °C. La salida esperada está registrada en `tests/salida_demo_pruebas.txt`.

## Estructura

```text
├── src/            Código fuente
├── tests/          Datos y resultados de prueba
├── docs/           Documentación y bitácora de prompts
├── evidencias/     Capturas y evidencias del proyecto
└── presentation/   Presentación del equipo
```

## Equipo

- Abril Miranda Baltazar Varillas — liderazgo y entrega.
- Luis Bryan Rojas Rodríguez — repositorio e integración técnica.
- Mariana Córdova Sánchez — documentación.
- Francesco Romero Díaz — pruebas y aseguramiento de calidad.
- Josué David Vázquez Trujillo — investigación y lógica difusa.

## Créditos, fuentes y licencias

La versión actual utiliza exclusivamente la biblioteca estándar de Python. Las funciones de pertenencia y el promedio ponderado fueron implementados por el equipo con fines académicos. Antes de la entrega deberán agregarse las referencias consultadas por el responsable de investigación.

## Uso de inteligencia artificial

Se utilizó inteligencia artificial como apoyo para explicar conceptos, proponer la estructura inicial del prototipo, revisar el código y sugerir casos de prueba. El equipo verificó y adaptó las funciones de pertenencia, los textos y los resultados. Los prompts y las correcciones se encuentran en `docs/bitacora_prompts.txt`.

## Estado del proyecto

Prototipo funcional para la Entrega 1. La interfaz gráfica, la documentación definitiva y las pruebas formales se desarrollarán en las siguientes entregas.
