"""
componentes.py — Widgets reutilizables de la interfaz.
Principio SRP: Cada componente gestiona su propio estado visual.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk


class SelectorArchivo(ctk.CTkFrame):
    """Widget de selección de archivo con label, entry y botón browse."""

    def __init__(
        self,
        master,
        titulo: str,
        tipos_archivo: list[tuple[str, str]] | None = None,
        es_carpeta: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)
        self._tipos = tipos_archivo or []
        self._es_carpeta = es_carpeta

        self.configure(fg_color="transparent")

        ctk.CTkLabel(
            self, text=titulo, font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", pady=(0, 4))

        fila = ctk.CTkFrame(self, fg_color="transparent")
        fila.pack(fill="x")

        self._entry = ctk.CTkEntry(fila, placeholder_text="Sin seleccionar…")
        self._entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        ctk.CTkButton(
            fila,
            text="Explorar",
            width=100,
            command=self._abrir_dialogo,
        ).pack(side="right")

    def _abrir_dialogo(self) -> None:
        if self._es_carpeta:
            ruta = filedialog.askdirectory(title="Selecciona carpeta de destino")
        else:
            ruta = filedialog.askopenfilename(
                title="Selecciona un archivo",
                filetypes=self._tipos or [("Todos los archivos", "*.*")],
            )
        if ruta:
            self._entry.delete(0, tk.END)
            self._entry.insert(0, ruta)

    def obtener_ruta(self) -> str:
        return self._entry.get().strip()

    def deshabilitar(self) -> None:
        self._entry.configure(state="disabled")

    def habilitar(self) -> None:
        self._entry.configure(state="normal")


class BarraEstado(ctk.CTkFrame):
    """Barra de progreso con etiqueta de estado combinada."""

    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")

        self._etiqueta = ctk.CTkLabel(
            self,
            text="En espera…",
            font=ctk.CTkFont(size=12),
            text_color="gray",
        )
        self._etiqueta.pack(anchor="w", pady=(0, 4))

        self._barra = ctk.CTkProgressBar(self, mode="determinate")
        self._barra.set(0)
        self._barra.pack(fill="x")

    def actualizar(self, progreso: float, mensaje: str) -> None:
        """progreso: valor entre 0.0 y 1.0."""
        self._barra.set(progreso)
        self._etiqueta.configure(text=mensaje)


class PanelResultado(ctk.CTkFrame):
    """Panel que muestra la ruta del archivo instrumental generado."""

    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.configure(corner_radius=10)
        self._ocultar_por_defecto()

    def _ocultar_por_defecto(self) -> None:
        self._icono = ctk.CTkLabel(self, text="✅", font=ctk.CTkFont(size=24))
        self._icono.pack(pady=(16, 4))

        ctk.CTkLabel(
            self, text="Archivo generado:", font=ctk.CTkFont(size=12, weight="bold")
        ).pack()

        self._ruta_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=11), wraplength=500, text_color="#aaffaa"
        )
        self._ruta_label.pack(padx=16, pady=(2, 16))

    def mostrar(self, ruta: str) -> None:
        self._ruta_label.configure(text=ruta)
        self.pack(fill="x", padx=24, pady=(0, 16))

    def ocultar(self) -> None:
        self.pack_forget()
