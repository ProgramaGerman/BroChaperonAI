"""
convertidor_formato.py — Conversión de audio entre formatos.
Principio SRP: Su única responsabilidad es convertir archivos de audio.
Usa ffmpeg (incluido en imageio-ffmpeg) para la conversión.
"""

import subprocess
from pathlib import Path

from imageio_ffmpeg import get_ffmpeg_exe

from logica.modelos import FormatoSalida


class ConvertidorFormato:
    """
    Convierte un archivo WAV al formato de salida elegido por el usuario.
    Respeta SRP: solo convierte, no separa ni gestiona video.
    """

    _BITRATE_MP3 = "192k"
    _BITRATE_M4A = "192k"

    def convertir(self, ruta_wav: str, formato: FormatoSalida) -> str:
        """
        Convierte `ruta_wav` al formato indicado.
        Retorna la ruta del archivo convertido.
        Si el formato es WAV, devuelve la misma ruta sin hacer nada.
        """
        if formato == FormatoSalida.WAV:
            return ruta_wav

        ruta_entrada = Path(ruta_wav)
        ruta_salida = ruta_entrada.with_suffix(formato.extension)

        ffmpeg = get_ffmpeg_exe()
        comando = self._construir_comando(ffmpeg, ruta_entrada, ruta_salida, formato)

        subprocess.run(comando, check=True, capture_output=True)
        return str(ruta_salida)

    # ─── Helpers privados ────────────────────────────────────────────────────

    def _construir_comando(
        self,
        ffmpeg: str,
        entrada: Path,
        salida: Path,
        formato: FormatoSalida,
    ) -> list[str]:
        base = [ffmpeg, "-y", "-i", str(entrada)]

        if formato == FormatoSalida.MP3:
            return base + ["-codec:a", "libmp3lame", "-b:a", self._BITRATE_MP3, str(salida)]

        if formato == FormatoSalida.M4A:
            return base + ["-codec:a", "aac", "-b:a", self._BITRATE_M4A, str(salida)]

        return base + [str(salida)]
