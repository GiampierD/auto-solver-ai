import os
import time
import random
import threading
import pyautogui
from core.capture import take_screenshot
from core.ai_engine import solve_autonomous

# Configuración de seguridad: mover el ratón a una esquina de la pantalla aborta de emergencia
pyautogui.FAILSAFE = True

# Estado del agente autónomo
_is_running = threading.Event()
_agent_thread = None
_preguntas_resueltas = 0

def _interruptible_sleep(seconds: float):
    """Pausa en pequeños intervalos para responder de inmediato si el usuario cancela."""
    elapsed = 0.0
    step = 0.1
    while elapsed < seconds:
        if not _is_running.is_set():
            return False
        time.sleep(step)
        elapsed += step
    return True

def _autonomous_worker():
    """Bucle principal de ejecución del agente autónomo."""
    global _preguntas_resueltas
    _preguntas_resueltas = 0
    
    screen_width, screen_height = pyautogui.size()
    print("\n" + "="*50)
    print("   🤖 AGENTE AUTÓNOMO INICIADO (MANOS LIBRES)   ")
    print("="*50)
    print("El agente resolverá y avanzará automáticamente.")
    print("Para DETENER en cualquier momento:")
    print(" - Presiona 'ctrl+shift+3' o 'esc'")
    print(" - O mueve el cursor bruscamente a una esquina de la pantalla (Failsafe)")
    print("="*50 + "\n")

    while _is_running.is_set():
        ciclo_inicio = time.time()
        print(f"\n[AGENTE] --- Procesando Pregunta #{_preguntas_resueltas + 1} ---")
        
        # 1. Capturar pantalla
        img_path = take_screenshot("auto_capture.png")
        if not _is_running.is_set():
            break

        if not img_path or not os.path.exists(img_path):
            print("[ERROR] No se pudo capturar la pantalla.")
            break

        # 2. Inferencia 2-en-1 (Opción + Botón de avance)
        resultado = solve_autonomous(img_path)
        
        # Limpieza inmediata de la imagen
        try:
            os.remove(img_path)
        except Exception:
            pass

        if not _is_running.is_set():
            break

        # 3. Validar si ya terminó el examen
        if not resultado:
            print("[WARNING] La IA no devolvió un formato válido. Reintentando en 2s...")
            if not _interruptible_sleep(2.0):
                break
            continue

        if resultado.get("es_fin_examen") is True:
            print("\n" + "*"*50)
            print(f"🎉 ¡EXAMEN FINALIZADO! Total resueltas: {_preguntas_resueltas}")
            print("*"*50 + "\n")
            break

        # 4. Obtener y ejecutar clic en la opción correcta
        coords_opcion = resultado.get("coordenadas_opcion")
        letra = resultado.get("letra_correcta", "N/A")

        if coords_opcion and len(coords_opcion) == 4 and any(coords_opcion):
            # Centroide de la opción
            centro_x_norm = (coords_opcion[1] + coords_opcion[3]) / 2
            centro_y_norm = (coords_opcion[0] + coords_opcion[2]) / 2
            
            pixel_opcion_x = int((centro_x_norm * screen_width) / 1000)
            pixel_opcion_y = int((centro_y_norm * screen_height) / 1000)
            
            print(f"[AGENTE] Opción seleccionada: [{letra}] en ({pixel_opcion_x}, {pixel_opcion_y})")
            
            try:
                pyautogui.moveTo(
                    pixel_opcion_x, 
                    pixel_opcion_y, 
                    duration=random.uniform(0.3, 0.45), 
                    tween=pyautogui.easeInOutQuad
                )
                pyautogui.click()
            except pyautogui.FailSafeException:
                print("\n[ALERTA] Failsafe activado por el usuario. Deteniendo agente...")
                break

            _preguntas_resueltas += 1
        else:
            print("[WARNING] No se ubicó la opción correcta en la pantalla.")

        # Pausa humana natural entre seleccionar la opción y presionar 'Siguiente'
        pausa_humana = random.uniform(0.8, 1.2)
        if not _interruptible_sleep(pausa_humana):
            break

        # 5. Obtener y ejecutar clic en el botón 'Siguiente'
        coords_sig = resultado.get("coordenadas_siguiente")
        if coords_sig and len(coords_sig) == 4 and any(coords_sig):
            sig_x_norm = (coords_sig[1] + coords_sig[3]) / 2
            sig_y_norm = (coords_sig[0] + coords_sig[2]) / 2
            
            pixel_sig_x = int((sig_x_norm * screen_width) / 1000)
            pixel_sig_y = int((sig_y_norm * screen_height) / 1000)
            
            print(f"[AGENTE] Avanzando: Clic en 'Siguiente' en ({pixel_sig_x}, {pixel_sig_y})")
            
            try:
                pyautogui.moveTo(
                    pixel_sig_x, 
                    pixel_sig_y, 
                    duration=random.uniform(0.25, 0.4), 
                    tween=pyautogui.easeInOutQuad
                )
                pyautogui.click()
            except pyautogui.FailSafeException:
                print("\n[ALERTA] Failsafe activado por el usuario. Deteniendo agente...")
                break
        else:
            print("[INFO] El botón 'Siguiente' no fue localizado en la vista actual. Desplazando scroll...")
            try:
                pyautogui.scroll(-300)
            except Exception:
                pass

        # Pausa para permitir que el navegador web procese y renderice la siguiente pregunta
        tiempo_ciclo = time.time() - ciclo_inicio
        print(f"[AGENTE] Pregunta #{_preguntas_resueltas} completada en {tiempo_ciclo:.1f}s. Esperando carga...")
        if not _interruptible_sleep(random.uniform(1.6, 2.2)):
            break

    _is_running.clear()
    print("\n[INFO] Modo Autónomo DETENIDO.")
    print(f"[RESUMEN] Total de preguntas resueltas en esta sesión: {_preguntas_resueltas}\n")

def toggle_autonomous_mode():
    """Activa o desactiva el agente autónomo con el mismo atajo de teclado."""
    global _agent_thread
    if _is_running.is_set():
        print("\n[INFO] Solicitando detención del Modo Autónomo...")
        _is_running.clear()
    else:
        _is_running.set()
        _agent_thread = threading.Thread(target=_autonomous_worker, daemon=True)
        _agent_thread.start()

def stop_autonomous():
    """Detiene el agente autónomo de inmediato."""
    if _is_running.is_set():
        _is_running.clear()
