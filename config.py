import os
import sys
import ctypes
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def setup_dpi_awareness():
    """
    Configura la resolución nativa de Windows 1:1 evitando desfases de escala (DPI Virtualization).
    Garantiza que mss y pyautogui operen exactamente en el mismo espacio físico de píxeles.
    """
    if sys.platform == "win32":
        try:
            # PROCESS_PER_MONITOR_DPI_AWARE_V2 = 2 (Windows 10 Creators Update+)
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
            print("[SISTEMA] Calibración DPI: Modo Per-Monitor V2 (1:1 nativo activado).")
        except Exception:
            try:
                # Fallback para versiones previas de Windows: PROCESS_SYSTEM_DPI_AWARE = 1
                ctypes.windll.user32.SetProcessDPIAware()
                print("[SISTEMA] Calibración DPI: Modo System DPI Aware activado.")
            except Exception as e:
                print(f"[WARNING] No se pudo configurar DPI awareness: {e}")
