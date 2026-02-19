"""
modelos.py — Modelos de datos del dominio.
Principio SRP: Este módulo solo define estructuras de datos.
"""

from dataclasses import dataclass, field
from enum import Enum


class FormatoSalida(Enum):
    """Formatos de audio disponibles para el archivo instrumental de salida."""
    WAV = "wav"
    MP3 = "mp3"
    M4A = "m4a"

    @property
    def extension(self) -> str:
        return f".{self.value}"

    @property
    def etiqueta(self) -> str:
        etiquetas = {"wav": "WAV (sin pérdida)", "mp3": "MP3", "m4a": "M4A (AAC)"}
        return etiquetas[self.value]

    @classmethod
    def desde_etiqueta(cls, etiqueta: str) -> "FormatoSalida":
        for f in cls:
            if f.etiqueta == etiqueta:
                return f
        return cls.WAV

    @classmethod
    def etiquetas(cls) -> list[str]:
        return [f.etiqueta for f in cls]


@dataclass
class ResultadoProcesamiento:
    """Encapsula el resultado de una operación de separación vocal."""
    exitoso: bool
    ruta_salida: str = ""
    mensaje_error: str = ""


@dataclass
class FormatosCompatibles:
    """Formatos de archivo soportados por la aplicación."""
    audio: tuple[str, ...] = field(default_factory=lambda: (".mp3", ".wav", ".flac", ".ogg", ".m4a"))
    video: tuple[str, ...] = field(default_factory=lambda: (".mp4", ".mkv", ".avi", ".mov", ".webm"))

    def es_audio(self, ruta: str) -> bool:
        return any(ruta.lower().endswith(ext) for ext in self.audio)

    def es_video(self, ruta: str) -> bool:
        return any(ruta.lower().endswith(ext) for ext in self.video)

    def es_compatible(self, ruta: str) -> bool:
        return self.es_audio(ruta) or self.es_video(ruta)

    def extensiones_para_dialogo(self) -> list[tuple[str, str]]:
        """Retorna la lista de tipos para el diálogo de selección de archivos."""
        audio_ext = " ".join(f"*{e}" for e in self.audio)
        video_ext = " ".join(f"*{e}" for e in self.video)
        return [
            ("Archivos de audio", audio_ext),
            ("Archivos de video", video_ext),
            ("Todos los archivos", "*.*"),
        ]
