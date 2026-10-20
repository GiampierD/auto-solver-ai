# Auto-Solver Multimodal con IA Espacial & RPA

Sistema de Automatización Robótica de Procesos (**RPA**) impulsado por Inteligencia Artificial Multimodal (**Vision-Language Models**). Diseñado para operar en segundo plano, interpretar preguntas complejas de opción múltiple directamente desde la interfaz gráfica del monitor y ejecutar acciones físicas automatizadas en tiempo real.

---

## Objetivos y Valor Académico

1. **Superación del OCR Tradicional:** Sustituye los motores de reconocimiento óptico de caracteres (Tesseract, binarización Otsu, heurísticas de parsing) por inferencia directa mediante **Gemini Vision**, garantizando resiliencia ante modos oscuros, tipografías variables y elementos gráficos.
2. **Comprensión Espacial Multimodal (*Spatial Understanding*):** Demuestra que la IA no solo comprende el contenido semántico del examen, sino también la geometría de la interfaz mediante la predicción de cajas delimitadoras (*Bounding Boxes*) normalizadas (`[ymin, xmin, ymax, xmax]`).
3. **Calibración Milimétrica de Hardware:** Implementa *Windows Per-Monitor DPI Awareness V2* para evitar desfases causados por el escalado de pantalla (125%, 150%) en laptops o monitores de alta resolución.
4. **Automatización Física:** Cierra el ciclo sensorial-motor traduciendo las coordenadas abstractas de la IA en movimientos de ratón suaves (curvas de aceleración cuadrática) y clics físicos en el navegador.

---

## Modos de Operación y Atajos Globales

El sistema escucha eventos de teclado en segundo plano sin interrumpir la ventana activa del navegador:

| Atajo | Modo | Descripción |
| :--- | :--- | :--- |
| `Ctrl + Shift + 1` | **Modo Informativo** *(Asistente)* | Despliega una tarjeta flotante minimalista (*HUD Always-on-Top*) en tema claro en la esquina superior de la pantalla. Muestra la opción sugerida, el texto clave y la **justificación teórica fundamentada**. |
| `Ctrl + Shift + 2` | **Modo Interactivo** *(Auto-clic)* | Envía un prompt ultrarrápido sin justificación para inferir únicamente las coordenadas espaciales y ejecutar un clic físico en la opción correcta. |
| `Ctrl + Shift + 3` | **Modo Autónomo** *(Manos Libres)* | Inicia un agente secuencial de bucle cerrado. En una sola inferencia 2-en-1 detecta la opción correcta y el botón *"Siguiente ➜"*, marcando y avanzando continuamente por las 40 preguntas hasta finalizar. Presionar nuevamente para pausar. |
| `Esc` | **Detener / Salir** | Cancela cualquier proceso en ejecución y cierra el programa de forma segura. |

> [!TIP]
> **Failsafe de Emergencia:** Si el Modo Autónomo está activo y necesitas tomar el control manual del ratón, basta con desplazar el cursor bruscamente a cualquier esquina de la pantalla para abortar la automatización de inmediato.

---

## Arquitectura del Proyecto

```text
auto_solver_project/
│
├── core/
│   ├── ai_engine.py       # Cliente Gemini, optimización de prompts y parsing robusto de JSON
│   └── capture.py         # Captura de pantalla a alta velocidad mediante mss
│
├── modes/
│   ├── informative.py     # Modo 1: Ventana flotante (HUD Tkinter) Always-on-Top
│   ├── interactive.py     # Modo 2: Mapeo de coordenadas espaciales y clic puntual
│   └── autonomous.py      # Modo 3: Bucle del agente autónomo continuo con delays humanos
│
├── config.py              # Calibración nativa de DPI en Windows y variables de entorno
├── main.py                # Orquestador del sistema y registro de atajos de teclado globales
├── ver_modelos.py         # Script utilitario de diagnóstico para consultar cuotas y modelos de la API
│
├── .env.example           # Plantilla de variables de entorno (sin credenciales privadas)
├── .gitignore             # Exclusión de entornos virtuales, claves y capturas temporales
└── requirements.txt       # Dependencias mínimas esenciales (codificado en UTF-8)
```

---

## Instalación y Puesta en Marcha

### 1. Requisitos Previos
- **Sistema Operativo:** Windows 10 u 11 (recomendado para la integración DPI y atajos globales).
- **Python:** Versión 3.10, 3.11 o 3.12.
- **Clave de API:** Una clave gratuita de [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Clonar el Repositorio
```bash
git clone https://github.com/GiampierD/auto-solver-ai
cd auto_solver_project
```

### 3. Crear y Activar el Entorno Virtual
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 4. Instalar Dependencias
```powershell
pip install -r requirements.txt
```

### 5. Configurar Credenciales
Copia la plantilla `.env.example` para crear tu archivo `.env`:
```powershell
Copy-Item .env.example .env
```
Abre `.env` y coloca tu clave de API:
```env
GEMINI_API_KEY=tu_clave_de_gemini_aqui
```

### 6. Ejecutar el Proyecto
```powershell
python main.py
```

---

## Descargo de Responsabilidad (Academic Disclaimer)

Este proyecto ha sido desarrollado con **fines estrictamente académicos, de investigación en accesibilidad asistiva e ingeniería de software**. Su propósito es el estudio práctico de la integración de Modelos Fundacionales de Visión y Lenguaje (VLM) con herramientas de Automatización Robótica de Procesos (RPA). El autor no promueve ni se responsabiliza por el uso indebido de este software en evaluaciones oficiales o con fines contrarios a las normas de conducta ética académica.
