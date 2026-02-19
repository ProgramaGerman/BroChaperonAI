"""
procesador_video.py — Extracción y combinación de audio en archivos de video.
Principio SRP: Solo maneja la conversión entre video y audio.
"""

from pathlib import Path
import tempfile

from moviepy import VideoFileClip, AudioFileClip

from logica.modelos import ResultadoProcesamiento
from logica.separador_audio import ISeparadorAudio


class ProcesadorVideo:
    """
    Orquesta el flujo completo para archivos de video:
      1. Extrae el audio del video.
      2. Delega la separación vocal al separador provisto (ISeparadorAudio).
      3. Combina el video original con el audio instrumental resultante.

    SRP: Su única responsabilidad es coordinar la pipeline audio↔video.
    """

    def __init__(self, separador: ISeparadorAudio) -> None:
        self._separador = separador

    def procesar(self, ruta_video: str, carpeta_salida: str) -> ResultadoProcesamiento:
        video_path = Path(ruta_video)
        salida_path = Path(carpeta_salida)
        salida_path.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory() as dir_temp:
            audio_temp = Path(dir_temp) / f"{video_path.stem}_audio.wav"
            carpeta_sep = Path(dir_temp) / "separado"

            try:
                self._extraer_audio(ruta_video, str(audio_temp))
            except Exception as e:
                return ResultadoProcesamiento(exitoso=False, mensaje_error=f"Error al extraer audio: {e}")

            resultado_sep = self._separador.separar(str(audio_temp), str(carpeta_sep))
            if not resultado_sep.exitoso:
                return resultado_sep

            ruta_final = salida_path / f"{video_path.stem}_instrumental{video_path.suffix}"
            try:
                self._combinar_video_audio(ruta_video, resultado_sep.ruta_salida, str(ruta_final))
            except Exception as e:
                return ResultadoProcesamiento(exitoso=False, mensaje_error=f"Error al combinar video: {e}")

        return ResultadoProcesamiento(exitoso=True, ruta_salida=str(ruta_final))

    # ─── Métodos privados ────────────────────────────────────────────────────

    def _extraer_audio(self, ruta_video: str, ruta_audio_salida: str) -> None:
        clip = VideoFileClip(ruta_video)
        if clip.audio is None:
            clip.close()
            raise ValueError("El video no contiene pista de audio.")
        clip.audio.write_audiofile(ruta_audio_salida, logger=None)
        clip.close()

    def _combinar_video_audio(
        self, ruta_video: str, ruta_audio: str, ruta_salida: str
    ) -> None:
        video = VideoFileClip(ruta_video)
        audio = AudioFileClip(ruta_audio)
        video_final = video.with_audio(audio)
        video_final.write_videofile(ruta_salida, logger=None, audio_codec="aac")
        video.close()
        audio.close()
