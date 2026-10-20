import os
import pyautogui
from core.capture import take_screenshot
from core.ai_engine import solve_interactive

def run_interactive_mode():
    """Ejecución del Modo Interactivo (Auto-clic mediante visión espacial)."""
    print("\n[INFO] Ejecutando Versión 2: Modo Interactivo (Auto-clic ultrarrápido)...")
    
    # 1. Obtener resolución del monitor principal
    screen_width, screen_height = pyautogui.size()
    
    # 2. Captura de pantalla
    img_path = take_screenshot()
    
    # 3. Inferencia optimizada con prompt interactivo (solo coordenadas y opción)
    if img_path and os.path.exists(img_path):
        resultado = solve_interactive(img_path)
        
        if resultado and "coordenadas" in resultado:
            coords = resultado["coordenadas"]  # [ymin, xmin, ymax, xmax] normalizadas de 0 a 1000
            letra = resultado.get("letra_correcta", "N/A")
            
            print(f"\n[INFO] IA seleccionó la opción: {letra}")
            print(f"[INFO] Bounding Box (Gemini): {coords}")
            
            # Calcular el punto central de la caja delimitadora
            centro_x_norm = (coords[1] + coords[3]) / 2
            centro_y_norm = (coords[0] + coords[2]) / 2
            
            # Mapeo a píxeles físicos del monitor
            pixel_x = int((centro_x_norm * screen_width) / 1000)
            pixel_y = int((centro_y_norm * screen_height) / 1000)
            
            print(f"[ACCIÓN] Desplazando cursor a X:{pixel_x}, Y:{pixel_y} y ejecutando clic...")
            
            # Movimiento natural con aceleración suave (0.4s) y clic físico
            pyautogui.moveTo(pixel_x, pixel_y, duration=0.4, tween=pyautogui.easeInOutQuad)
            pyautogui.click()
            print("[SUCCESS] Clic completado.")
        else:
            print("[ERROR] No se pudieron obtener las coordenadas espaciales de la opción.")
            
        # 4. Limpieza de captura temporal
        try:
            os.remove(img_path)
            print("[INFO] Captura temporal eliminada.")
        except Exception as e:
            print(f"[WARNING] No se pudo eliminar la imagen temporal: {e}")
            
    print("[SUCCESS] Proceso interactivo completado.")
