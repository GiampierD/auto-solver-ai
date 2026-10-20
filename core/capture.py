import mss
import mss.tools
import os

def take_screenshot(filename="temp_capture.png"):
    print("[INFO] Capturando la pantalla...")
    with mss.mss() as sct:
        # Captura el monitor principal. Si tienes dos pantallas, monitor 1 es la principal.
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        
        # Guarda la imagen en la raíz del proyecto temporalmente
        output_path = os.path.join(os.getcwd(), filename)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_path)
        
        return output_path