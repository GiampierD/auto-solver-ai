import os
import tkinter as tk
import threading
from core.capture import take_screenshot
from core.ai_engine import solve_informative

def show_info_popup(letra: str, texto: str, justificacion: str, duration: int = 9):
    """
    Despliega una tarjeta flotante HUD con paleta de colores claros,
    alto contraste y diseño moderno (Always-on-Top).
    """
    def _create_window():
        root = tk.Tk()
        root.title("Auto-Solver HUD")
        
        # Mantener siempre al frente y sin marcos toscos del sistema
        root.attributes("-topmost", True)
        root.overrideredirect(True)
        
        # Paleta de colores claros profesional (Modern SaaS / Clean UI)
        bg_card = "#ffffff"           # Fondo blanco limpio
        border_color = "#cbd5e1"      # Borde sutil grafito (slate-300)
        header_color = "#393A3B"      # Azul profesional (blue-600)
        badge_bg = "#dcfce7"          # Fondo verde menta suave (emerald-100)
        badge_fg = "#15803d"          # Texto verde esmeralda oscuro (emerald-700)
        badge_border = "#86efac"      # Borde del badge (emerald-300)
        text_color = "#0f172a"        # Texto negro grafito de alto contraste (slate-900)
        box_just_bg = "#f8fafc"       # Fondo caja justificación (slate-50)
        box_just_border = "#e2e8f0"   # Borde caja justificación (slate-200)
        just_color = "#334155"        # Texto justificación gris oscuro (slate-700)
        
        width = 390
        height = 210
        
        # Posicionar en la esquina superior derecha
        screen_w = root.winfo_screenwidth()
        pos_x = screen_w - width - 25
        pos_y = 35
        root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
        
        # Marco exterior contenedor para definir el contorno sobre fondos blancos
        outer_border = tk.Frame(root, bg=border_color, padx=1, pady=1)
        outer_border.pack(fill="both", expand=True)
        
        card = tk.Frame(outer_border, bg=bg_card, padx=14, pady=10)
        card.pack(fill="both", expand=True)
        
        # 1. Header (Título + Botón cerrar ✕)
        header_frame = tk.Frame(card, bg=bg_card)
        header_frame.pack(fill="x")
        
        lbl_title = tk.Label(
            header_frame, 
            text="💡 AUTO-SOLVER  |  ASISTENTE", 
            font=("Segoe UI", 8, "bold"), 
            fg=header_color, 
            bg=bg_card
        )
        lbl_title.pack(side="left")
        
        btn_close = tk.Label(
            header_frame, 
            text="✕", 
            font=("Segoe UI", 10, "bold"), 
            fg="#94a3b8", 
            bg=bg_card, 
            cursor="hand2"
        )
        btn_close.pack(side="right")
        btn_close.bind("<Button-1>", lambda e: root.destroy())
        btn_close.bind("<Enter>", lambda e: btn_close.config(fg="#ef4444"))
        btn_close.bind("<Leave>", lambda e: btn_close.config(fg="#94a3b8"))
        
        # 2. Badge de la opción correcta
        badge_frame = tk.Frame(card, bg=bg_card)
        badge_frame.pack(fill="x", pady=(5, 3))
        
        badge_border_frame = tk.Frame(badge_frame, bg=badge_border, padx=1, pady=1)
        badge_border_frame.pack(side="left")
        
        lbl_badge = tk.Label(
            badge_border_frame, 
            text=f"  OPCIÓN CORRECTA:  {letra}  ", 
            font=("Segoe UI", 10, "bold"), 
            fg=badge_fg, 
            bg=badge_bg,
            padx=6,
            pady=2
        )
        lbl_badge.pack()
        
        # 3. Texto de la respuesta seleccionada
        lbl_text = tk.Label(
            card, 
            text=texto, 
            font=("Segoe UI", 9, "bold"), 
            fg=text_color, 
            bg=bg_card, 
            wraplength=360, 
            justify="left"
        )
        lbl_text.pack(anchor="w", pady=(3, 5))
        
        # 4. Tarjeta interior para la Justificación
        just_container = tk.Frame(card, bg=box_just_border, padx=1, pady=1)
        just_container.pack(fill="x", pady=(2, 0))
        
        just_inner = tk.Frame(just_container, bg=box_just_bg, padx=8, pady=6)
        just_inner.pack(fill="both", expand=True)
        
        lbl_just = tk.Label(
            just_inner, 
            text=f"Fundamento: {justificacion}", 
            font=("Segoe UI", 8), 
            fg=just_color, 
            bg=box_just_bg, 
            wraplength=345, 
            justify="left"
        )
        lbl_just.pack(anchor="w")
        
        # Auto-destrucción tras 'duration' segundos
        root.after(int(duration * 1000), root.destroy)
        
        # Permitir arrastrar la ventana libremente
        def start_move(event):
            root.x = event.x
            root.y = event.y

        def do_move(event):
            deltax = event.x - root.x
            deltay = event.y - root.y
            x = root.winfo_x() + deltax
            y = root.winfo_y() + deltay
            root.geometry(f"+{x}+{y}")

        card.bind("<ButtonPress-1>", start_move)
        card.bind("<B1-Motion>", do_move)
        
        root.mainloop()

    # Ejecutar en hilo secundario daemon para no congelar los atajos
    threading.Thread(target=_create_window, daemon=True).start()

def run_informative_mode():
    """Ejecución del Modo Informativo (Asistente visual con tarjeta flotante)."""
    print("\n[INFO] Ejecutando Versión 1: Modo Informativo...")
    
    # 1. Captura de pantalla
    img_path = take_screenshot()
    
    # 2. Inferencia optimizada con prompt informativo
    if img_path and os.path.exists(img_path):
        resultado = solve_informative(img_path)
        
        if resultado:
            letra = resultado.get("letra_correcta", "N/A")
            texto = resultado.get("texto_opcion", "N/A")
            justificacion = resultado.get("justificacion", "Sin justificación disponible.")
            
            # Imprimir en consola de respaldo
            print("\n" + "="*45)
            print("           RESULTADO DE LA IA           ")
            print("="*45)
            print(f"Opción Correcta : {letra}")
            print(f"Respuesta       : {texto}")
            print(f"Justificación   : {justificacion}")
            print("="*45 + "\n")
            
            # 3. Lanzar la ventana flotante con tema claro
            show_info_popup(letra, texto, justificacion, duration=9)
        else:
            print("[ERROR] No se pudo obtener la respuesta de la IA.")
        
        # 4. Limpieza de captura temporal
        try:
            os.remove(img_path)
            print("[INFO] Captura temporal eliminada.")
        except Exception as e:
            print(f"[WARNING] No se pudo eliminar la imagen temporal: {e}")
            
    print("[SUCCESS] Proceso informativo completado.")
