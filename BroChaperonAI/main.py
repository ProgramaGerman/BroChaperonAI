# =============================================================================
# main.py — Punto de entrada de BroChaperonAI
# =============================================================================

from dotenv import load_dotenv

load_dotenv()   # Carga .env antes de instanciar AIEngine

from app.models.ai_engine import AIEngine
from app.models.image_processor import ImageProcessor
from app.presenters.chat_presenter import ChatPresenter
from app.views.main_window import MainWindow


def main() -> None:
    """Inicializa la aplicación y arranca el bucle de eventos."""
    try:
        engine    = AIEngine()
    except EnvironmentError as exc:
        # Mostrar ventana mínima de error si falta la API key
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("BroChaperonAI — Configuración", str(exc))
        root.destroy()
        return

    processor = ImageProcessor()
    view      = MainWindow()
    presenter = ChatPresenter(view)
    view.set_presenter(presenter)
    view.mainloop()


if __name__ == "__main__":
    main()
