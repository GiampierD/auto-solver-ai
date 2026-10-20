import os
import json
import re
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY no encontrada en las variables de entorno (.env)")

genai.configure(api_key=api_key)

# Modelo recomendado por cuota (15 RPM / 500 RPD) y alta velocidad
MODEL_NAME = "models/gemini-3.5-flash-lite"

def _clean_and_parse_json(raw_text: str):
    """Extrae y parsea de forma segura el bloque JSON devuelto por Gemini."""
    text = raw_text.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    else:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            text = match.group(0)
    return json.loads(text)

def solve_informative(image_path: str):
    """
    Modo Informativo:
    Pide la respuesta correcta, el texto de la opción y la justificación teórica.
    No solicita coordenadas espaciales para ahorrar tokens y acelerar la inferencia.
    """
    print("[INFO] Analizando imagen para Modo Informativo (con justificación)...")
    model = genai.GenerativeModel(MODEL_NAME)
    
    prompt = """
    Eres un asistente experto resolviendo exámenes de conocimientos y reglas de tránsito.
    En la imagen se muestra una pregunta de opción múltiple.
    1. Identifica la opción correcta (letra y texto).
    2. Proporciona una justificación breve, clara y fundamentada de por qué esa es la respuesta correcta.
    
    Devuelve ÚNICAMENTE un objeto JSON estrictamente con este formato:
    {
        "letra_correcta": "A",
        "texto_opcion": "Texto de la respuesta",
        "justificacion": "Breve explicación fundamentada"
    }
    """
    
    try:
        img = Image.open(image_path)
        response = model.generate_content([prompt, img])
        return _clean_and_parse_json(response.text)
    except Exception as e:
        print(f"[ERROR] Error en inferencia informativa: {e}")
        return None

def solve_interactive(image_path: str):
    """
    Modo Interactivo (Auto-clic puntual):
    Pide la opción correcta y sus coordenadas espaciales normalizadas [ymin, xmin, ymax, xmax].
    NO solicita justificación teórica, optimizando al máximo los tokens de salida y la velocidad.
    """
    print("[INFO] Analizando imagen para Modo Interactivo (cálculo de coordenadas espaciales)...")
    model = genai.GenerativeModel(MODEL_NAME)
    
    prompt = """
    Eres un agente autónomo de automatización de exámenes de opción múltiple.
    En la imagen se muestra una pregunta de opción múltiple.
    1. Identifica la opción correcta.
    2. Localiza las coordenadas espaciales (Bounding Box) de la letra de la opción correcta o de su casilla/círculo de selección.
    
    Devuelve ÚNICAMENTE un objeto JSON estrictamente con este formato. Las coordenadas deben ser [ymin, xmin, ymax, xmax] normalizadas de 0 a 1000:
    {
        "letra_correcta": "A",
        "coordenadas": [ymin, xmin, ymax, xmax]
    }
    """
    
    try:
        img = Image.open(image_path)
        response = model.generate_content([prompt, img])
        return _clean_and_parse_json(response.text)
    except Exception as e:
        print(f"[ERROR] Error en inferencia interactiva: {e}")
        return None

def solve_autonomous(image_path: str):
    """
    Modo Autónomo (Inferencia 2-en-1):
    En una sola llamada detecta:
    1. Si es fin de examen o pantalla final.
    2. La opción correcta y sus coordenadas espaciales.
    3. Las coordenadas espaciales del botón de avance ('Siguiente' o 'Finalizar').
    
    Ahorra tokens al resolver ambos elementos en una sola pasada.
    """
    print("[INFO] Analizando pantalla para Modo Autónomo (Opción + Botón de avance)...")
    model = genai.GenerativeModel(MODEL_NAME)
    
    prompt = """
    Eres un agente autónomo de RPA para resolver exámenes de opción múltiple.
    Analiza la imagen de la pantalla actual:
    1. Determina si hay una pregunta activa de opción múltiple o si ya finalizó el examen (pantalla de resultados, nota o finalizado).
    2. Si hay pregunta activa:
       - Identifica la opción correcta.
       - Localiza las coordenadas espaciales [ymin, xmin, ymax, xmax] (0-1000) de la letra de la opción correcta o de su casilla/círculo de selección.
       - Localiza las coordenadas espaciales [ymin, xmin, ymax, xmax] (0-1000) del botón de avance (usualmente dice "Siguiente", "Siguiente ➜" o "Finalizar").
    
    Devuelve ÚNICAMENTE un objeto JSON estrictamente con este formato:
    {
        "es_fin_examen": false,
        "letra_correcta": "A",
        "coordenadas_opcion": [ymin, xmin, ymax, xmax],
        "coordenadas_siguiente": [ymin, xmin, ymax, xmax]
    }
    
    Si la pantalla muestra que el examen ya terminó o una tabla de resultados finales:
    {
        "es_fin_examen": true,
        "mensaje": "Examen finalizado"
    }
    """
    
    try:
        img = Image.open(image_path)
        response = model.generate_content([prompt, img])
        return _clean_and_parse_json(response.text)
    except Exception as e:
        print(f"[ERROR] Error en inferencia autónoma: {e}")
        return None

def solve_question(image_path: str, mode: str = "informative"):
    """Función de compatibilidad para enrutar según el modo solicitado."""
    if mode == "interactive":
        return solve_interactive(image_path)
    elif mode == "autonomous":
        return solve_autonomous(image_path)
    return solve_informative(image_path)
