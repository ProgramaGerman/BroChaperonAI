# =============================================================================
# main_window.py — Vista principal BroChaperonAI (Rediseño Equipo Alejabot)
# [Especialista-Frontend] Layout 2 col · Panel resoluciones · 6 modos · Texto visible
# Convención: imports alfabéticos · atributos por longitud ascendente
#             métodos por longitud de nombre ascendente
# =============================================================================

import tkinter as tk
from tkinter import filedialog, messagebox
from typing import TYPE_CHECKING, Callable

import customtkinter as ctk
from PIL import Image

if TYPE_CHECKING:
    from app.presenters.chat_presenter import ChatPresenter

# ---------------------------------------------------------------------------
# Paleta de colores — más visible y contrastada
# ---------------------------------------------------------------------------
BG_ROOT:     str = "#09090F"   # negro puro del fondo
BG_CARD:     str = "#111118"   # tarjetas ligeramente más claras
BG_CARD2:    str = "#0D0D16"   # zona de respuesta / upload
BG_SIDEBAR:  str = "#0F0F1A"   # fondo del panel lateral
BORDER_OFF:  str = "#252538"   # borde inactivo (más visible que antes)
BORDER_ON:   str = "#7C3AED"   # borde activo / seleccionado (púrpura)
ACCENT_DIM:  str = "#5B21B6"   # hover modos activos
TXT_MAIN:    str = "#F0F0FF"   # texto principal (más brillante)
TXT_MID:     str = "#AAAACC"   # texto medio — labels de botones (más claro)
TXT_DIM:     str = "#666680"   # texto tenue (subtítulos, footer)
TXT_SECTION: str = "#8888BB"   # títulos de sección
WHITE:       str = "#FFFFFF"

# Resoluciones disponibles (ancho, alto) con etiqueta
RESOLUTIONS: list[tuple[str, int, int]] = [
    ("1280×720  HD",       1280, 720),
    ("1366×768  HD+",      1366, 768),
    ("1920×1080  Full HD", 1920, 1080),
    ("1600×900  HD+",      1600, 900),
]
DEFAULT_RES_IDX: int = 2   # Full HD seleccionado por defecto

# Ícono unicode por modo
MODE_ICONS: dict[str, str] = {
    "provocativo":   "🔥",
    "enamorar":      "💕",
    "salvada_epica": "⚡",
    "coquetear":     "😏",
    "rompehielo":    "🧊",
    "modo_amigos":   "👥",
}

MODE_LABELS: dict[str, str] = {
    "provocativo":   "PROVOCATIVO",
    "enamorar":      "ENAMORAR",
    "salvada_epica": "SALVADA ÉPICA",
    "coquetear":     "COQUETEAR",
    "rompehielo":    "ROMPEHIELO",
    "modo_amigos":   "MODO AMIGOS",
}

# Agrupación de modos por sección
MODES_ROW1: list[str] = ["provocativo", "enamorar", "salvada_epica", "coquetear"]
MODES_ROW2: list[str] = ["rompehielo", "modo_amigos"]


# ---------------------------------------------------------------------------
# Widget auxiliar — tarjeta con borde personalizable
# ---------------------------------------------------------------------------

class _BorderCard(ctk.CTkFrame):
    """Frame con borde de 1 px usando un frame exterior como borde."""

    def __init__(self, master, border_color: str = BORDER_OFF, **kwargs):
        cr_outer = kwargs.pop("corner_radius", 14)
        super().__init__(master, fg_color=border_color, corner_radius=cr_outer)
        self._inner = ctk.CTkFrame(
            self,
            fg_color=kwargs.pop("fg_color", BG_CARD),
            corner_radius=cr_outer - 1,
            **kwargs,
        )
        self._inner.pack(fill="both", expand=True, padx=1, pady=1)

    def inner(self) -> ctk.CTkFrame:
        return self._inner

    def set_border(self, color: str) -> None:
        self.configure(fg_color=color)


# ===========================================================================
# MainWindow
# ===========================================================================

class MainWindow(ctk.CTk):
    """Vista principal de BroChaperonAI — Rediseño Equipo Alejabot."""

    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self._ctk_img: ctk.CTkImage | None          = None
        self.presenter: "ChatPresenter | None"       = None
        self._active_mode: str | None                = None
        self._active_res_idx: int                    = DEFAULT_RES_IDX
        self._mode_cards: dict[str, _BorderCard]     = {}
        self._res_cards: list[_BorderCard]           = []

        self._build_window()
        self._build_layout()

    # --- set_presenter ---------------------------------------------------
    def set_presenter(self, presenter: "ChatPresenter") -> None:
        self.presenter = presenter

    # --- show_error ------------------------------------------------------
    def show_error(self, msg: str) -> None:
        messagebox.showerror("BroChaperonAI", msg, parent=self)

    # --- set_status ------------------------------------------------------
    def set_status(self, text: str) -> None:
        self._status_var.set(text)

    # --- show_preview ----------------------------------------------------
    def show_preview(self, image: Image.Image) -> None:
        self._ctk_img = ctk.CTkImage(
            light_image=image, dark_image=image, size=(68, 68)
        )
        self._upload_icon_lbl.configure(image=self._ctk_img, text="")
        self._upload_title.configure(text="PANTALLAZO CARGADO ✓")
        self._upload_sub.configure(text="Motor de análisis listo")

    # --- show_response ---------------------------------------------------
    def show_response(self, text: str) -> None:
        self._response_box.configure(state="normal")
        self._response_box.delete("1.0", "end")
        self._response_box.insert("1.0", f'"{text}"')
        self._response_box.configure(state="disabled")

    # --- set_loading -----------------------------------------------------
    def set_loading(self, active: bool) -> None:
        if active:
            self._progress.pack(pady=(0, 6))
            self._progress.start()
        else:
            self._progress.stop()
            self._progress.pack_forget()
        self._set_modes_state("disabled" if active else "normal")

    # =========================================================================
    # Builders — estructura de 2 columnas
    # =========================================================================

    def _build_window(self) -> None:
        w, h = RESOLUTIONS[DEFAULT_RES_IDX][1], RESOLUTIONS[DEFAULT_RES_IDX][2]
        self.title("BroChaperonAI")
        self.geometry(f"{w}x{h}")
        self.minsize(900, 680)
        self.configure(fg_color=BG_ROOT)
        # 2 columnas: col 0 = contenido principal (flex), col 1 = sidebar fijo
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0, minsize=240)
        self.grid_rowconfigure(0, weight=1)

    def _build_layout(self) -> None:
        """Crea el frame izquierdo (principal) y el panel derecho (sidebar)."""
        # ----- Panel izquierdo -----
        self._left = ctk.CTkFrame(self, fg_color=BG_ROOT)
        self._left.grid(row=0, column=0, sticky="nsew", padx=(16, 8), pady=16)
        self._left.grid_columnconfigure(0, weight=1)
        self._left.grid_rowconfigure(3, weight=1)   # fila respuesta crece

        self._build_header(self._left)
        self._build_upload_zone(self._left)
        self._build_mode_buttons(self._left)
        self._build_response_area(self._left)
        self._build_copy_button(self._left)
        self._build_footer(self._left)

        # ----- Panel derecho (sidebar) -----
        self._right = ctk.CTkFrame(
            self, fg_color=BG_SIDEBAR,
            corner_radius=16,
        )
        self._right.grid(row=0, column=1, sticky="nsew", padx=(0, 16), pady=16)
        self._right.grid_columnconfigure(0, weight=1)
        self._build_sidebar(self._right)

    # ---- Header -------------------------------------------------------
    def _build_header(self, parent) -> None:
        hdr = ctk.CTkFrame(parent, fg_color="transparent", height=54)
        hdr.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        hdr.grid_columnconfigure(0, weight=1)

        inner = ctk.CTkFrame(hdr, fg_color="transparent")
        inner.grid(row=0, column=0)

        ctk.CTkLabel(
            inner, text="⬤",
            font=ctk.CTkFont("Segoe UI", 18),
            text_color="#8B5CF6",
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            inner,
            text="BRO CHAPERON  AI",
            font=ctk.CTkFont("Segoe UI", 17, "bold"),
            text_color=TXT_MAIN,
        ).pack(side="left")

    # ---- Upload zone ---------------------------------------------------
    def _build_upload_zone(self, parent) -> None:
        card = _BorderCard(parent, border_color=BORDER_OFF, corner_radius=16)
        card.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        inner = card.inner()
        inner.configure(fg_color=BG_CARD2, cursor="hand2")

        for w in (inner, card):
            w.bind("<Button-1>", lambda e: self._on_load_click())

        self._upload_icon_lbl = ctk.CTkLabel(
            inner, text="📷",
            font=ctk.CTkFont("Segoe UI", 38),
            text_color=TXT_MID,
        )
        self._upload_icon_lbl.pack(pady=(20, 4))
        self._upload_icon_lbl.bind("<Button-1>", lambda e: self._on_load_click())

        self._upload_title = ctk.CTkLabel(
            inner,
            text="CARGAR PANTALLAZO",
            font=ctk.CTkFont("Segoe UI", 14, "bold"),
            text_color=TXT_MAIN,
        )
        self._upload_title.pack()
        self._upload_title.bind("<Button-1>", lambda e: self._on_load_click())

        self._upload_sub = ctk.CTkLabel(
            inner,
            text="Haz clic para seleccionar tu captura de pantalla",
            font=ctk.CTkFont("Segoe UI", 10),
            text_color=TXT_MID,
        )
        self._upload_sub.pack(pady=(3, 18))
        self._upload_sub.bind("<Button-1>", lambda e: self._on_load_click())

        self._progress = ctk.CTkProgressBar(
            inner, mode="indeterminate",
            progress_color=BORDER_ON, height=2, width=280,
        )

    # ---- Mode buttons --------------------------------------------------
    def _build_mode_buttons(self, parent) -> None:
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        container.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Etiqueta de sección
        self._build_section_label(container, "MODO DE RESPUESTA", col_span=4, row=0)

        # — Fila 1: 4 modos románticos —
        row1 = ctk.CTkFrame(container, fg_color="transparent")
        row1.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(4, 4))
        row1.grid_columnconfigure((0, 1, 2, 3), weight=1)
        for col, key in enumerate(MODES_ROW1):
            self._build_mode_card(row1, key, col, 0)

        # — Fila 2: 2 modos sociales (más anchos) —
        row2 = ctk.CTkFrame(container, fg_color="transparent")
        row2.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(0, 4))
        row2.grid_columnconfigure((0, 1), weight=1)
        for col, key in enumerate(MODES_ROW2):
            self._build_mode_card(row2, key, col, 0, tall=False)

    def _build_section_label(self, parent, text: str, col_span: int = 1, row: int = 0) -> None:
        ctk.CTkLabel(
            parent, text=text,
            font=ctk.CTkFont("Segoe UI", 9, "bold"),
            text_color=TXT_SECTION,
        ).grid(row=row, column=0, columnspan=col_span, sticky="w", padx=4, pady=(4, 0))

    def _build_mode_card(self, parent, key: str, col: int, row: int, tall: bool = True) -> None:
        card = _BorderCard(parent, border_color=BORDER_OFF, corner_radius=12)
        card.grid(row=row, column=col, padx=4, pady=0, sticky="nsew")
        inner = card.inner()
        inner.configure(fg_color=BG_CARD, cursor="hand2")

        icon_lbl = ctk.CTkLabel(
            inner,
            text=MODE_ICONS[key],
            font=ctk.CTkFont("Segoe UI", 22),
            text_color=TXT_MID,
        )
        icon_lbl.pack(pady=(16, 4) if tall else (12, 4))

        lbl = ctk.CTkLabel(
            inner,
            text=MODE_LABELS[key],
            font=ctk.CTkFont("Segoe UI", 9, "bold"),
            text_color=TXT_MID,
        )
        lbl.pack(pady=(0, 14) if tall else (0, 12))

        for widget in (card, inner, icon_lbl, lbl):
            widget.bind("<Button-1>", lambda e, k=key: self._on_mode_click(k))

        self._mode_cards[key] = card

    # ---- Response area ------------------------------------------------
    def _build_response_area(self, parent) -> None:
        # Sección label
        lbl_row = ctk.CTkFrame(parent, fg_color="transparent")
        lbl_row.grid(row=3, column=0, sticky="ew")
        ctk.CTkLabel(
            lbl_row, text="RESPUESTA GENERADA",
            font=ctk.CTkFont("Segoe UI", 9, "bold"),
            text_color=TXT_SECTION,
        ).pack(side="left", padx=4, pady=(4, 0))

        card = _BorderCard(parent, border_color=BORDER_OFF, corner_radius=16)
        card.grid(row=3, column=0, sticky="nsew", pady=(2, 0))
        parent.grid_rowconfigure(3, weight=1)
        inner = card.inner()
        inner.configure(fg_color=BG_CARD2)
        inner.grid_rowconfigure(0, weight=1)
        inner.grid_columnconfigure(0, weight=1)

        self._response_box = ctk.CTkTextbox(
            inner,
            font=ctk.CTkFont("Georgia", 14, slant="italic"),
            text_color=TXT_MAIN,
            fg_color="transparent",
            corner_radius=0,
            wrap="word",
            state="disabled",
            border_width=0,
        )
        self._response_box.pack(fill="both", expand=True, padx=24, pady=24)

    # ---- Copy button --------------------------------------------------
    def _build_copy_button(self, parent) -> None:
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.grid(row=4, column=0, pady=(12, 6))

        ctk.CTkButton(
            btn_frame,
            text="📋  COPIAR RESPUESTA",
            font=ctk.CTkFont("Segoe UI", 12, "bold"),
            text_color="#09090F",
            fg_color=WHITE,
            hover_color="#D4D4E8",
            corner_radius=50,
            height=42,
            width=260,
            command=self._on_copy_click,
        ).pack()

    # ---- Footer -------------------------------------------------------
    def _build_footer(self, parent) -> None:
        foot = ctk.CTkFrame(parent, fg_color="transparent", height=32)
        foot.grid(row=5, column=0, sticky="ew", pady=(0, 4))
        foot.grid_columnconfigure(1, weight=1)

        self._status_var = tk.StringVar(value="")
        ctk.CTkLabel(
            foot,
            textvariable=self._status_var,
            font=ctk.CTkFont("Segoe UI", 9),
            text_color=TXT_DIM,
        ).grid(row=0, column=0, padx=4, sticky="w")

        ctk.CTkLabel(
            foot, text="BroChaperonAI  ·  Equipo Alejabot  ·  v2.0",
            font=ctk.CTkFont("Segoe UI", 8),
            text_color=TXT_DIM,
        ).grid(row=0, column=2, padx=4, sticky="e")

    # =========================================================================
    # Sidebar derecho — Panel de configuración
    # =========================================================================

    def _build_sidebar(self, parent) -> None:
        # Título del panel
        ctk.CTkLabel(
            parent,
            text="⚙️  CONFIG",
            font=ctk.CTkFont("Segoe UI", 13, "bold"),
            text_color="#9B6DFF",
        ).pack(anchor="w", padx=16, pady=(20, 2))

        # Separador
        ctk.CTkFrame(parent, fg_color=BORDER_OFF, height=1).pack(fill="x", padx=12, pady=(4, 16))

        # — Sección Resolución —
        ctk.CTkLabel(
            parent,
            text="RESOLUCIÓN DE VENTANA",
            font=ctk.CTkFont("Segoe UI", 9, "bold"),
            text_color=TXT_SECTION,
        ).pack(anchor="w", padx=16, pady=(0, 8))

        for i, (label, w, h) in enumerate(RESOLUTIONS):
            is_default = (i == DEFAULT_RES_IDX)
            border_col = BORDER_ON if is_default else BORDER_OFF
            card = _BorderCard(parent, border_color=border_col, corner_radius=10)
            card.pack(fill="x", padx=12, pady=3)
            inner = card.inner()
            inner.configure(
                fg_color="#1A1030" if is_default else BG_CARD,
                cursor="hand2",
            )

            lbl = ctk.CTkLabel(
                inner,
                text=label,
                font=ctk.CTkFont("Segoe UI", 10, "bold" if is_default else "normal"),
                text_color=TXT_MAIN if is_default else TXT_MID,
            )
            lbl.pack(pady=10, padx=10, anchor="w")

            for widget in (card, inner, lbl):
                widget.bind("<Button-1>", lambda e, idx=i: self._on_res_click(idx))

            self._res_cards.append(card)
            card._inner_ref = inner   # guardar ref del inner para actualizar color

        # Separador
        ctk.CTkFrame(parent, fg_color=BORDER_OFF, height=1).pack(fill="x", padx=12, pady=(20, 16))

        # — Info del modelo —
        ctk.CTkLabel(
            parent,
            text="MODELO IA",
            font=ctk.CTkFont("Segoe UI", 9, "bold"),
            text_color=TXT_SECTION,
        ).pack(anchor="w", padx=16, pady=(0, 4))

        ctk.CTkLabel(
            parent,
            text="Qwen3-VL 30B\nMultimodal Vision",
            font=ctk.CTkFont("Segoe UI", 10),
            text_color=TXT_MID,
            justify="left",
        ).pack(anchor="w", padx=20, pady=(0, 12))

        # — Estado del sistema —
        ctk.CTkFrame(parent, fg_color=BORDER_OFF, height=1).pack(fill="x", padx=12, pady=(0, 16))

        status_row = ctk.CTkFrame(parent, fg_color="transparent")
        status_row.pack(fill="x", padx=16, pady=(0, 20))

        ctk.CTkLabel(
            status_row, text="●",
            font=ctk.CTkFont("Segoe UI", 10),
            text_color="#22C55E",
        ).pack(side="left", padx=(0, 6))

        ctk.CTkLabel(
            status_row,
            text="Sistema listo",
            font=ctk.CTkFont("Segoe UI", 10),
            text_color=TXT_MID,
        ).pack(side="left")

    # =========================================================================
    # Callbacks
    # =========================================================================

    def _on_load_click(self) -> None:
        path = filedialog.askopenfilename(
            title="Seleccionar captura de pantalla",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png"), ("Todos", "*.*")],
        )
        if path and self.presenter:
            self.presenter.on_load(path)

    def _on_copy_click(self) -> None:
        text = self._response_box.get("1.0", "end").strip().strip('"')
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)

    def _on_mode_click(self, mode: str) -> None:
        """Resalta el modo activo y dispara la generación."""
        if self._active_mode and self._active_mode in self._mode_cards:
            self._mode_cards[self._active_mode].set_border(BORDER_OFF)
        self._active_mode = mode
        self._mode_cards[mode].set_border(BORDER_ON)
        if self.presenter:
            self.presenter.on_generate(mode)

    def _on_res_click(self, idx: int) -> None:
        """Cambia la resolución de la ventana y resalta la card seleccionada."""
        # Quitar selección anterior
        prev = self._active_res_idx
        if prev < len(self._res_cards):
            self._res_cards[prev].set_border(BORDER_OFF)
            inner = self._res_cards[prev]._inner_ref
            inner.configure(fg_color=BG_CARD)
            # Actualizar label del card anterior
            for w in inner.winfo_children():
                if isinstance(w, ctk.CTkLabel):
                    w.configure(text_color=TXT_MID, font=ctk.CTkFont("Segoe UI", 10))

        # Activar nuevo
        self._active_res_idx = idx
        self._res_cards[idx].set_border(BORDER_ON)
        inner_new = self._res_cards[idx]._inner_ref
        inner_new.configure(fg_color="#1A1030")
        for w in inner_new.winfo_children():
            if isinstance(w, ctk.CTkLabel):
                w.configure(text_color=TXT_MAIN, font=ctk.CTkFont("Segoe UI", 10, "bold"))

        # Aplicar resolución
        _, w, h = RESOLUTIONS[idx]
        self.geometry(f"{w}x{h}")

    def _make_mode_callback(self, mode: str) -> Callable[[], None]:
        return lambda: self._on_mode_click(mode)

    def _set_modes_state(self, state: str) -> None:
        """Habilita/deshabilita los clicks en las tarjetas de modo."""
        cursor = "hand2" if state == "normal" else "arrow"
        for card in self._mode_cards.values():
            card.inner().configure(cursor=cursor)
