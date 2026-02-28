# =============================================================================
# test_suite.py — Pruebas unitarias para AIEngine e ImageProcessor
# Ejecutar: python -m pytest tests/test_suite.py -v
#       o:  python -m unittest tests/test_suite.py -v
# =============================================================================

import io
import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from PIL import Image

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_rgb_image(w: int = 400, h: int = 600) -> Image.Image:
    """Crea una imagen RGB en memoria para las pruebas."""
    return Image.new("RGB", (w, h), color=(100, 150, 200))


# ===========================================================================
# TestImageProcessor
# ===========================================================================

class TestImageProcessor(unittest.TestCase):
    """Pruebas unitarias del módulo image_processor."""

    def setUp(self) -> None:
        # Importación dentro de setUp para aislar el módulo del entorno global
        from app.models.image_processor import ImageProcessor
        self.proc = ImageProcessor()

    # --- test_load_invalid (16) ---
    def test_load_invalid(self) -> None:
        """Debe lanzar ValueError al cargar un archivo con extensión no permitida."""
        with self.assertRaises(ValueError):
            self.proc.load("captura.bmp")

    # --- test_load_valid (14) ---
    def test_load_valid(self) -> None:
        """Debe cargar correctamente un archivo PNG temporal válido."""
        img = _make_rgb_image()
        tmp = Path("tests/_tmp_test.png")
        img.save(tmp)
        try:
            result = self.proc.load(tmp)
            self.assertIsInstance(result, Image.Image)
        finally:
            tmp.unlink(missing_ok=True)

    # --- test_resize_bounds (17) ---
    def test_resize_bounds(self) -> None:
        """El lado más largo de la imagen redimensionada no debe superar max_px."""
        img    = _make_rgb_image(2000, 3000)
        result = self.proc.resize(img, max_px=1024)
        self.assertLessEqual(max(result.size), 1024)

    # --- test_thumbnail_size (18) ---
    def test_thumbnail_size(self) -> None:
        """La miniatura debe tener exactamente el tamaño solicitado."""
        img    = _make_rgb_image(800, 600)
        thumb  = self.proc.to_thumbnail(img, size=(200, 200))
        self.assertEqual(thumb.size, (200, 200))


# ===========================================================================
# TestAIEngine
# ===========================================================================

class TestAIEngine(unittest.TestCase):
    """Pruebas unitarias del módulo ai_engine."""

    # --- test_missing_key (15) ---
    def test_missing_key(self) -> None:
        """Debe lanzar EnvironmentError si OPENROUTER_API_KEY no está definida."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("OPENROUTER_API_KEY", None)
            from importlib import reload
            import app.models.ai_engine as eng_mod
            reload(eng_mod)   # forzar recarga sin variable
            with self.assertRaises(EnvironmentError):
                eng_mod.AIEngine()

    # --- test_invalid_mode (16) ---
    def test_invalid_mode(self) -> None:
        """Debe lanzar ValueError al pedir un modo de arquetipo desconocido."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            from importlib import reload
            import app.models.ai_engine as eng_mod
            reload(eng_mod)
            engine = eng_mod.AIEngine()
            img    = _make_rgb_image()
            with self.assertRaises(ValueError):
                engine.ask(img, "modo_inexistente")

    # --- test_payload_structure (22) ---
    def test_payload_structure(self) -> None:
        """El payload generado debe contener las claves obligatorias para OpenRouter."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            from importlib import reload
            import app.models.ai_engine as eng_mod
            reload(eng_mod)
            engine  = eng_mod.AIEngine()
            img     = _make_rgb_image()
            payload = engine._build_payload(img, "coquetear")

            self.assertIn("model",      payload)
            self.assertIn("messages",   payload)
            self.assertIn("max_tokens", payload)
            self.assertTrue(len(payload["messages"]) >= 2)


if __name__ == "__main__":
    unittest.main()
