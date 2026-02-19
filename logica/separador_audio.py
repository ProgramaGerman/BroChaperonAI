"""
separador_audio.py — Interfaz e implementación de separación vocal.
Principios SOLID aplicados:
  - ISP: ISeparadorAudio define solo lo que necesita el presentador.
  - SRP: La clase solo separa audio, no hace nada más.
"""

from typing import Protocol
from pathlib import Path
import subprocess
import sys

from logica.modelos import ResultadoProcesamiento

# Ruta al wrapper que parchea torchaudio.load antes de invocar demucs
_WRAPPER = Path(__file__).parent / "_demucs_wrapper.py"


class ISeparadorAudio(Protocol):
    """
    Interfaz de separación de audio (Interface Segregation Principle).
    Cualquier implementación debe proveer únicamente este método.
    """

    def separar(self, ruta_entrada: str, carpeta_salida: str) -> ResultadoProcesamiento:
        """Separa voces de un archivo de audio y guarda el instrumental."""
        ...


class DemucsAudioSeparator:
    """
    Implementación real de separación vocal usando Demucs (Meta AI).
    Respeta SRP: su única responsabilidad es invocar demucs y retornar el resultado.
    Usa _demucs_wrapper.py para evitar la dependencia de torchcodec en torchaudio 2.10+.
    """

    MODELO = "htdemucs"

    def separar(self, ruta_entrada: str, carpeta_salida: str) -> ResultadoProcesamiento:
        ruta = Path(ruta_entrada)
        salida = Path(carpeta_salida)
        salida.mkdir(parents=True, exist_ok=True)

        try:
            subprocess.run(
                [
                    sys.executable,
                    str(_WRAPPER),
                    "--two-stems", "vocals",
                    "-n", self.MODELO,
                    "-o", str(salida),
                    str(ruta),
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            ruta_instrumental = self._buscar_instrumental(salida, ruta.stem)
            return ResultadoProcesamiento(exitoso=True, ruta_salida=str(ruta_instrumental))

        except subprocess.CalledProcessError as e:
            return ResultadoProcesamiento(exitoso=False, mensaje_error=e.stderr or str(e))
        except FileNotFoundError as e:
            return ResultadoProcesamiento(exitoso=False, mensaje_error=str(e))

    def _buscar_instrumental(self, carpeta_salida: Path, nombre_stem: str) -> Path:
        """Localiza el archivo 'no_vocals.wav' generado por demucs."""
        patron = carpeta_salida / self.MODELO / nombre_stem / "no_vocals.wav"
        if patron.exists():
            return patron
        # Búsqueda recursiva como fallback
        candidatos = list(carpeta_salida.rglob("no_vocals.wav"))
        if candidatos:
            return candidatos[0]
        raise FileNotFoundError(
            f"No se encontró el archivo instrumental en: {carpeta_salida}"
        )
