"""
ventana_principal.py — Ventana principal de la aplicación.
La Vista en MVP: solo presenta datos y delega eventos al Presentador.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import customtkinter as ctk
from tkinter import messagebox

from logica.modelos import FormatoSalida
from vista.componentes import SelectorArchivo, BarraEstado, PanelResultado

if TYPE_CHECKING:
    from controlador.presentador import Presentador


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class VentanaPrincipal(ctk.CTk):
    """
    Ventana principal de la aplicación Vocal Remover.
    Responsabilidad única (SRP): gestionar la interfaz de usuario.
    """

    TITULO = "Vocal Remover 🎵"
    ANCHO = 680
    ALTO = 640

    def __init__(self, presentador: Presentador) -> None:
        super().__init__()
        self._presentador = presentador
        self._presentador.vincular_vista(self)
        self._construir_ui()
        self._centrar_ventana()

    # ─── Construcción de la UI ───────────────────────────────────────────────

    def _construir_ui(self) -> None:
        self.title(self.TITULO)
        self.geometry(f"{self.ANCHO}x{self.ALTO}")
        self.resizable(False, False)

        self._construir_encabezado()
        self._construir_cuerpo()
        self._construir_pie()

    def _construir_encabezado(self) -> None:
        encabezado = ctk.CTkFrame(self, fg_color=("#1a1a2e", "#0f0f1a"), corner_radius=0)
        encabezado.pack(fill="x")

        ctk.CTkLabel(
            encabezado,
            text="🎵 Vocal Remover",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#4fc3f7",
        ).pack(pady=(18, 4))

        ctk.CTkLabel(
            encabezado,
            text="Elimina voces de canciones — soporta audio y video",
            font=ctk.CTkFont(size=13),
            text_color="gray",
        ).pack(pady=(0, 18))

    def _construir_cuerpo(self) -> None:
        self._cuerpo = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self._cuerpo.pack(fill="both", expand=True, padx=24, pady=16)

        tipos = self._presentador.obtener_formatos_dialogo()

        self._selector_archivo = SelectorArchivo(
            self._cuerpo,
            titulo="📂  Archivo de entrada (audio o video)",
            tipos_archivo=tipos,
        )
        self._selector_archivo.pack(fill="x", pady=(0, 16))

        self._selector_salida = SelectorArchivo(
            self._cuerpo,
            titulo="📁  Carpeta de destino",
            es_carpeta=True,
        )
        self._selector_salida.pack(fill="x", pady=(0, 20))

        # ── Selector de formato de salida ────────────────────────────────────
        self._construir_selector_formato()

        self._boton_procesar = ctk.CTkButton(
            self._cuerpo,
            text="▶  Procesar",
            height=46,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#1565c0",
            hover_color="#0d47a1",
            command=self._on_click_procesar,
        )
        self._boton_procesar.pack(fill="x", pady=(0, 20))

        self._barra_estado = BarraEstado(self._cuerpo)
        self._barra_estado.pack(fill="x", pady=(0, 12))

        self._panel_resultado = PanelResultado(self._cuerpo, fg_color=("#1b2a1b", "#0d1a0d"))

    def _construir_selector_formato(self) -> None:
        """Panel con selector de formato de salida usando botones segmentados."""
        contenedor = ctk.CTkFrame(self._cuerpo, fg_color="transparent")
        contenedor.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            contenedor,
            text="🎚  Formato de salida",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).pack(anchor="w", pady=(0, 8))

        etiquetas = self._presentador.obtener_formatos_salida()
        self._formato_var = ctk.StringVar(value=etiquetas[0])

        self._selector_formato = ctk.CTkSegmentedButton(
            contenedor,
            values=etiquetas,
            variable=self._formato_var,
            font=ctk.CTkFont(size=13),
            height=38,
            selected_color="#1565c0",
            selected_hover_color="#0d47a1",
        )
        self._selector_formato.pack(fill="x")

    def _construir_pie(self) -> None:
        ctk.CTkLabel(
            self,
            text="Powered by Demucs (Meta AI)  •  HTDemucs model",
            font=ctk.CTkFont(size=10),
            text_color="gray",
        ).pack(pady=(0, 10))

    # ─── Métodos de la interfaz pública (usados por el Presentador) ──────────

    def actualizar_progreso(self, valor: float, mensaje: str) -> None:
        self._barra_estado.actualizar(valor, mensaje)

    def mostrar_resultado(self, ruta_salida: str) -> None:
        self._panel_resultado.mostrar(ruta_salida)

    def mostrar_error(self, mensaje: str) -> None:
        messagebox.showerror("Error", mensaje, parent=self)

    def deshabilitar_controles(self) -> None:
        self._boton_procesar.configure(state="disabled", text="⏳  Procesando…")
        self._selector_archivo.deshabilitar()
        self._selector_salida.deshabilitar()
        self._selector_formato.configure(state="disabled")
        self._panel_resultado.ocultar()

    def habilitar_controles(self) -> None:
        self._boton_procesar.configure(state="normal", text="▶  Procesar")
        self._selector_archivo.habilitar()
        self._selector_salida.habilitar()
        self._selector_formato.configure(state="normal")

    # ─── Eventos internos ────────────────────────────────────────────────────

    def _on_click_procesar(self) -> None:
        formato = FormatoSalida.desde_etiqueta(self._formato_var.get())
        self._presentador.on_procesar(
            self._selector_archivo.obtener_ruta(),
            self._selector_salida.obtener_ruta(),
            formato,
        )

    def _centrar_ventana(self) -> None:
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.ANCHO) // 2
        y = (self.winfo_screenheight() - self.ALTO) // 2
        self.geometry(f"{self.ANCHO}x{self.ALTO}+{x}+{y}")
