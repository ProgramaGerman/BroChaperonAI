"""
presentador.py — Presentador del patrón MVP.
Conecta la Vista (CTk UI) con la Lógica (separador + procesador + convertidor).
Corre el procesamiento en un hilo secundario para no bloquear la UI.
"""

from __future__ import annotations

import threading
from pathlib import Path
from typing import TYPE_CHECKING

from logica.modelos import FormatosCompatibles, FormatoSalida, ResultadoProcesamiento
from logica.separador_audio import DemucsAudioSeparator
from logica.procesador_video import ProcesadorVideo
from logica.convertidor_formato import ConvertidorFormato

if TYPE_CHECKING:
    from vista.ventana_principal import VentanaPrincipal


class Presentador:
    """
    Orquesta la comunicación entre Vista y Modelo.
    Respeta SRP: su única responsabilidad es coordinar el flujo de la aplicación.
    """

    def __init__(self) -> None:
        self._formatos = FormatosCompatibles()
        self._separador = DemucsAudioSeparator()
        self._procesador_video = ProcesadorVideo(self._separador)
        self._convertidor = ConvertidorFormato()
        self._vista: VentanaPrincipal | None = None

    def vincular_vista(self, vista: VentanaPrincipal) -> None:
        """Registra la vista para poder actualizarla."""
        self._vista = vista

    # ─── Eventos de la Vista ─────────────────────────────────────────────────

    def on_procesar(
        self,
        ruta_archivo: str,
        carpeta_salida: str,
        formato_salida: FormatoSalida,
    ) -> None:
        """Llamado por la Vista cuando el usuario presiona 'Procesar'."""
        if not self._validar_entrada(ruta_archivo, carpeta_salida):
            return

        self._vista.deshabilitar_controles()
        self._vista.actualizar_progreso(0.05, "Iniciando procesamiento…")

        hilo = threading.Thread(
            target=self._procesar_en_hilo,
            args=(ruta_archivo, carpeta_salida, formato_salida),
            daemon=True,
        )
        hilo.start()

    # ─── Consultas auxiliares para la Vista ──────────────────────────────────

    def obtener_formatos_dialogo(self) -> list[tuple[str, str]]:
        return self._formatos.extensiones_para_dialogo()

    def obtener_formatos_salida(self) -> list[str]:
        return FormatoSalida.etiquetas()

    # ─── Lógica privada ──────────────────────────────────────────────────────

    def _validar_entrada(self, ruta_archivo: str, carpeta_salida: str) -> bool:
        if not ruta_archivo:
            self._vista.mostrar_error("Selecciona un archivo de audio o video.")
            return False
        if not carpeta_salida:
            self._vista.mostrar_error("Selecciona una carpeta de destino.")
            return False
        if not Path(ruta_archivo).exists():
            self._vista.mostrar_error("El archivo seleccionado no existe.")
            return False
        if not self._formatos.es_compatible(ruta_archivo):
            self._vista.mostrar_error(
                f"Formato no soportado. Usa: "
                f"{', '.join(self._formatos.audio + self._formatos.video)}"
            )
            return False
        return True

    def _procesar_en_hilo(
        self,
        ruta_archivo: str,
        carpeta_salida: str,
        formato_salida: FormatoSalida,
    ) -> None:
        try:
            self._vista.actualizar_progreso(0.15, "Separando voces con Demucs (puede tardar)…")

            if self._formatos.es_video(ruta_archivo):
                resultado = self._procesador_video.procesar(ruta_archivo, carpeta_salida)
            else:
                resultado = self._separador.separar(ruta_archivo, carpeta_salida)

            if resultado.exitoso and formato_salida != FormatoSalida.WAV:
                self._vista.after(
                    0,
                    lambda: self._vista.actualizar_progreso(0.92, f"Convirtiendo a {formato_salida.value.upper()}…"),
                )
                ruta_convertida = self._convertidor.convertir(
                    resultado.ruta_salida, formato_salida
                )
                resultado = ResultadoProcesamiento(exitoso=True, ruta_salida=ruta_convertida)

            self._vista.after(0, lambda: self._on_procesamiento_completo(resultado))
        except Exception as e:
            self._vista.after(
                0,
                lambda: self._on_procesamiento_completo(
                    ResultadoProcesamiento(exitoso=False, mensaje_error=str(e))
                ),
            )

    def _on_procesamiento_completo(self, resultado: ResultadoProcesamiento) -> None:
        self._vista.habilitar_controles()
        if resultado.exitoso:
            self._vista.actualizar_progreso(1.0, "¡Listo!")
            self._vista.mostrar_resultado(resultado.ruta_salida)
        else:
            self._vista.actualizar_progreso(0.0, "Error")
            self._vista.mostrar_error(resultado.mensaje_error)
