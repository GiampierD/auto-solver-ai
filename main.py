import config

# 1. Calibración milimétrica de DPI en Windows
config.setup_dpi_awareness()

import keyboard
from modes.informative import run_informative_mode
from modes.interactive import run_interactive_mode
from modes.autonomous import toggle_autonomous_mode, stop_autonomous

def on_exit():
    """Cierre seguro del programa deteniendo cualquier hilo activo."""
    print("\n[INFO] Cerrando programa de forma segura...")
    stop_autonomous()

def main():
    print("========================================")
    print("      AUTO-SOLVER PROJECT INICIADO      ")
    print("========================================")
    print("Atajos globales disponibles:")
    print(" - 'ctrl+shift+1': Modo Informativo (HUD Flotante)")
    print(" - 'ctrl+shift+2': Modo Interactivo (Auto-clic puntual)")
    print(" - 'ctrl+shift+3': Modo Autónomo (Manos Libres: Resuelve y Avanza)")
    print(" - 'esc': Detener / Salir del programa")
    print("========================================")
    print("Escuchando en segundo plano...\n")

    # Registro de atajos de teclado globales
    keyboard.add_hotkey('ctrl+shift+1', run_informative_mode)
    keyboard.add_hotkey('ctrl+shift+2', run_interactive_mode)
    keyboard.add_hotkey('ctrl+shift+3', toggle_autonomous_mode)

    # Esperar hasta presionar 'esc' para salir
    keyboard.wait('esc')
    on_exit()
    print("[SUCCESS] Auto-Solver finalizado.")

if __name__ == "__main__":
    main()
