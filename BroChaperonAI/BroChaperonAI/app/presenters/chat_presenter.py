# =============================================================================
# chat_presenter.py — Presentador MVP: orquesta Modelo ↔ Vista
# Convención: imports alfabéticos · atributos por longitud ascendente
#             métodos por longitud de nombre ascendente
# =============================================================================

import threading
from pathlib import Path
from typing import TYPE_CHECKING

from app.models.ai_engine import AIEngine
from app.models.image_processor import ImageProcessor

if TYPE_CHECKING:
    from app.views.main_window import MainWindow


class ChatPresenter:
    """Intermediario entre la Vista y los Modelos de IA e imagen."""

    # Atributos por longitud ascendente: view(4) · engine(6) · processor(9)
    def __init__(self, view: "MainWindow") -> None:
        self.view: "MainWindow"      = view
        self.engine: AIEngine        = AIEngine()
        self.processor: ImageProcessor = ImageProcessor()
        self._image                  = None   # PIL.Image activa

    # --- on_load (7) -------------------------------------------------------
    def on_load(self, path: str) -> None:
        """Carga la imagen desde disco y actualiza la previsualización en la Vista."""
        try:
            self._image = self.processor.load(path)
            resized     = self.processor.resize(self._image)
            thumbnail   = self.processor.to_thumbnail(resized)
            self.view.show_preview(thumbnail)
            self.view.set_status("✅ Imagen cargada. Elige un modo de respuesta.")
        except (ValueError, FileNotFoundError) as exc:
            self.view.show_error(str(exc))

    # --- on_generate (11) --------------------------------------------------
    def on_generate(self, mode: str) -> None:
        """Genera una respuesta de IA para el modo dado de forma asíncrona."""
        if self._image is None:
            self.view.show_error("⚠️ Carga una imagen antes de generar.")
            return
        self.view.set_loading(True)
        self.view.set_status(f"⏳ Generando respuesta '{mode}'…")
        threading.Thread(
            target=self._run_generation,
            args=(mode,),
            daemon=True,
        ).start()

    # --- _run_generation (15) ----------------------------------------------
    def _run_generation(self, mode: str) -> None:
        """Ejecuta la llamada a la IA en un hilo secundario y actualiza la Vista."""
        try:
            image_for_api = self.processor.resize(self._image)
            response      = self.engine.ask(image_for_api, mode)
            self.view.after(0, lambda: self._on_success(response, mode))
        except Exception as exc:  # noqa: BLE001
            err_msg = str(exc)   # capturar antes del lambda: Python 3 borra 'exc' al salir del bloque
            self.view.after(0, lambda: self._on_error(err_msg))

    # --- _on_error (9) -----------------------------------------------------
    def _on_error(self, message: str) -> None:
        """Maneja errores de generación en el hilo principal de la UI."""
        self.view.set_loading(False)
        self.view.show_error(message)
        self.view.set_status("❌ Error al generar. Revisa tu clave API o conexión.")

    # --- _on_success (10) --------------------------------------------------
    def _on_success(self, text: str, mode: str) -> None:
        """Muestra el resultado exitoso en el hilo principal de la UI."""
        self.view.set_loading(False)
        self.view.show_response(text)
        self.view.set_status(f"✅ Respuesta '{mode}' generada.")
