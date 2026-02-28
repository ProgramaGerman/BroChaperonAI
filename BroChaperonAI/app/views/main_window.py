# =============================================================================
# main_window.py — Vista principal rediseñada (estilo COUPLA AI)
# CustomTkinter dark premium · lógica intacta del presentador
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
# Paleta de colores (inspirada en el mockup)
# ---------------------------------------------------------------------------
BG_ROOT:    str = "#09090F"   # negro puro del fondo
BG_CARD:    str = "#111118"   # tarjetas ligeramente más claras
BG_CARD2:   str = "#0D0D14"   # zona de respuesta / upload
BORDER_OFF: str = "#1E1E2E"   # borde inactivo
BORDER_ON:  str = "#7C3AED"   # borde activo / seleccionado (púrpura)
TXT_MAIN:   str = "#E8E8F0"   # texto principal
TXT_DIM:    str = "#42425A"   # texto tenue (subtítulos, footer)
TXT_MID:    str = "#8888A8"   # texto medio (labels de botones)
WHITE:      str = "#FFFFFF"

# Ícono unicode por modo (sustituye SVG)
MODE_ICONS: dict[str, str] = {
    "provocativo":   "🔥",
    "enamorar":      "💕",
    "salvada_epica": "⚡",
    "coquetear":     "😏",
}

MODE_LABELS: dict[str, str] = {
    "provocativo":   "PROVOCATIVO",
    "enamorar":      "ENAMORAR",
    "salvada_epica": "SALVADA ÉPICA",
    "coquetear":     "COQUETEAR",
}


# ---------------------------------------------------------------------------
# Widget auxiliar — tarjeta con borde personalizable
# ---------------------------------------------------------------------------

class _BorderCard(ctk.CTkFrame):
    """Frame con borde de 1 px usando un frame exterior como borde."""

    def __init__(self, master, border_color: str = BORDER_OFF, **kwargs):
        # Frame exterior = borde
        super().__init__(
            master,
            fg_color=border_color,
            corner_radius=kwargs.pop("corner_radius", 14),
        )
        # Frame interior = contenido
        cr = kwargs.pop("corner_radius", 13)
        self._inner = ctk.CTkFrame(
            self,
            fg_color=kwargs.pop("fg_color", BG_CARD),
            corner_radius=cr,
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
    """Vista principal de BroChaperonAI — estilo COUPLA AI."""

    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Atributos por longitud ascendente
        self._ctk_img: ctk.CTkImage | None      = None
        self.presenter: "ChatPresenter | None"   = None
        self._active_mode: str | None            = None
        self._mode_cards: dict[str, _BorderCard] = {}

        self._build_window()
        self._build_header()
        self._build_upload_zone()
        self._build_mode_buttons()
        self._build_response_area()
        self._build_copy_button()
        self._build_footer()

    # --- set_presenter (13) ------------------------------------------------
    def set_presenter(self, presenter: "ChatPresenter") -> None:
        self.presenter = presenter

    # --- show_error (10) ---------------------------------------------------
    def show_error(self, msg: str) -> None:
        messagebox.showerror("BroChaperonAI", msg, parent=self)

    # --- set_status (10) ---------------------------------------------------
    def set_status(self, text: str) -> None:
        self._status_var.set(text)

    # --- show_preview (12) -------------------------------------------------
    def show_preview(self, image: Image.Image) -> None:
        """Reemplaza el ícono de carga con la miniatura de la imagen."""
        self._ctk_img = ctk.CTkImage(
            light_image=image, dark_image=image, size=(72, 72)
        )
        self._upload_icon_lbl.configure(image=self._ctk_img, text="")
        self._upload_title.configure(text="P A N T A L L A Z O   C A R G A D O")
        self._upload_sub.configure(text="M O T O R   D E   A N Á L I S I S   L I S T O  ·")

    # --- show_response (13) ------------------------------------------------
    def show_response(self, text: str) -> None:
        self._response_box.configure(state="normal")
        self._response_box.delete("1.0", "end")
        self._response_box.insert("1.0", f'"{text}"')
        self._response_box.configure(state="disabled")

    # --- set_loading (11) --------------------------------------------------
    def set_loading(self, active: bool) -> None:
        if active:
            self._progress.pack(pady=(0, 6))
            self._progress.start()
        else:
            self._progress.stop()
            self._progress.pack_forget()
        self._set_modes_state("disabled" if active else "normal")

    # ---- builders privados ------------------------------------------------

    def _build_window(self) -> None:
        self.title("BroChaperonAI")
        self.geometry("740x820")
        self.minsize(620, 720)
        self.configure(fg_color=BG_ROOT)
        self.grid_columnconfigure(0, weight=1)

    def _build_header(self) -> None:
        """Franja superior: orbe + título BroChaperonAI."""
        hdr = ctk.CTkFrame(self, fg_color=BG_ROOT, height=64)
        hdr.grid(row=0, column=0, sticky="ew", padx=0, pady=(20, 0))
        hdr.grid_columnconfigure(0, weight=1)

        # Contenedor centrado
        inner = ctk.CTkFrame(hdr, fg_color="transparent")
        inner.grid(row=0, column=0)

        # Orbe (círculo con gradiente simulado — emoji de esfera)
        orb = ctk.CTkLabel(
            inner, text="⬤",
            font=ctk.CTkFont("Segoe UI", 18),
            text_color="#8B5CF6",
        )
        orb.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            inner,
            text="B R O C H A P E R O N   A I",
            font=ctk.CTkFont("Segoe UI", 15, "bold"),
            text_color=TXT_MAIN,
        ).pack(side="left")

    def _build_upload_zone(self) -> None:
        """Zona de carga centrada con ícono de cámara."""
        card = _BorderCard(self, border_color=BORDER_OFF, corner_radius=18)
        card.grid(row=1, column=0, sticky="ew", padx=80, pady=(28, 0))
        inner = card.inner()
        inner.configure(fg_color=BG_CARD2, cursor="hand2")

        # Click en toda la tarjeta
        for w in (inner, card):
            w.bind("<Button-1>", lambda e: self._on_load_click())

        # Ícono cámara (texto unicode grande)
        self._upload_icon_lbl = ctk.CTkLabel(
            inner, text="📷",
            font=ctk.CTkFont("Segoe UI", 42),
            text_color=TXT_MID,
        )
        self._upload_icon_lbl.pack(pady=(28, 4))
        self._upload_icon_lbl.bind("<Button-1>", lambda e: self._on_load_click())

        self._upload_title = ctk.CTkLabel(
            inner,
            text="C A R G A R   P A N T A L L A Z O",
            font=ctk.CTkFont("Segoe UI", 13, "bold"),
            text_color=TXT_MAIN,
        )
        self._upload_title.pack()
        self._upload_title.bind("<Button-1>", lambda e: self._on_load_click())

        self._upload_sub = ctk.CTkLabel(
            inner,
            text="M O T O R   D E   A N Á L I S I S   L I S T O  ·",
            font=ctk.CTkFont("Segoe UI", 9),
            text_color=TXT_DIM,
        )
        self._upload_sub.pack(pady=(2, 24))
        self._upload_sub.bind("<Button-1>", lambda e: self._on_load_click())

        # Progress bar (oculto por defecto)
        self._progress = ctk.CTkProgressBar(
            inner, mode="indeterminate",
            progress_color=BORDER_ON, height=2, width=320,
        )

    def _build_mode_buttons(self) -> None:
        """Cuatro tarjetas cuadradas en fila horizontal."""
        row_frame = ctk.CTkFrame(self, fg_color="transparent")
        row_frame.grid(row=2, column=0, sticky="ew", padx=80, pady=(18, 0))
        row_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        for col, (key, label) in enumerate(MODE_LABELS.items()):
            card = _BorderCard(
                row_frame,
                border_color=BORDER_OFF,
                corner_radius=14,
            )
            card.grid(row=0, column=col, padx=5, pady=0, sticky="nsew")
            inner = card.inner()
            inner.configure(fg_color=BG_CARD, cursor="hand2")

            icon_lbl = ctk.CTkLabel(
                inner,
                text=MODE_ICONS[key],
                font=ctk.CTkFont("Segoe UI", 22),
                text_color=TXT_MID,
            )
            icon_lbl.pack(pady=(22, 6))

            lbl = ctk.CTkLabel(
                inner,
                text=label,
                font=ctk.CTkFont("Segoe UI", 8, "bold"),
                text_color=TXT_MID,
            )
            lbl.pack(pady=(0, 20))

            cb = self._make_mode_callback(key)
            for widget in (card, inner, icon_lbl, lbl):
                widget.bind("<Button-1>", lambda e, k=key: self._on_mode_click(k))

            self._mode_cards[key] = card

    def _build_response_area(self) -> None:
        """Área de texto grande con respuesta en cursiva centrada."""
        card = _BorderCard(self, border_color=BORDER_OFF, corner_radius=18)
        card.grid(row=3, column=0, sticky="nsew", padx=80, pady=(18, 0))
        self.grid_rowconfigure(3, weight=1)
        inner = card.inner()
        inner.configure(fg_color=BG_CARD2)
        inner.grid_rowconfigure(0, weight=1)
        inner.grid_columnconfigure(0, weight=1)

        self._response_box = ctk.CTkTextbox(
            inner,
            font=ctk.CTkFont("Georgia", 15, slant="italic"),
            text_color=TXT_MAIN,
            fg_color="transparent",
            corner_radius=0,
            wrap="word",
            state="disabled",
            border_width=0,
        )
        self._response_box.pack(fill="both", expand=True, padx=28, pady=28)

    def _build_copy_button(self) -> None:
        """Botón píldora blanco centrado."""
        btn_frame = ctk.CTkFrame(self, fg_color=BG_ROOT)
        btn_frame.grid(row=4, column=0, pady=(18, 6))

        ctk.CTkButton(
            btn_frame,
            text="📋  C O P I A R   R E S P U E S T A",
            font=ctk.CTkFont("Segoe UI", 11, "bold"),
            text_color="#09090F",
            fg_color=WHITE,
            hover_color="#D4D4E8",
            corner_radius=50,
            height=44,
            width=280,
            command=self._on_copy_click,
        ).pack()

    def _build_footer(self) -> None:
        """Barra inferior con etiquetas tipo NEURAL ARCHITECTURE."""
        foot = ctk.CTkFrame(self, fg_color=BG_ROOT, height=40)
        foot.grid(row=5, column=0, sticky="ew", padx=0, pady=(4, 12))
        foot.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            foot, text="E X C E L E N C I A   E N   I N T E R A C C I Ó N   H U M A N A",
            font=ctk.CTkFont("Segoe UI", 7), text_color=TXT_DIM,
        ).grid(row=0, column=0, padx=20, sticky="w")

        # Centro: separadores + texto
        mid = ctk.CTkFrame(foot, fg_color="transparent")
        mid.grid(row=0, column=1)
        ctk.CTkLabel(
            mid,
            text="—————  A R Q U I T E C T U R A   N E U R A L  —————",
            font=ctk.CTkFont("Segoe UI", 7),
            text_color=TXT_DIM,
        ).pack()

        ctk.CTkLabel(
            foot, text="P R O T O C O L O",
            font=ctk.CTkFont("Segoe UI", 7), text_color=TXT_DIM,
        ).grid(row=0, column=2, padx=20, sticky="e")

        # Barra de estado interna (invisible al usuario, solo para debug)
        self._status_var = tk.StringVar(value="")

    # ---- callbacks --------------------------------------------------------

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
        # Quitar borde del anterior
        if self._active_mode and self._active_mode in self._mode_cards:
            self._mode_cards[self._active_mode].set_border(BORDER_OFF)
        # Activar nuevo
        self._active_mode = mode
        self._mode_cards[mode].set_border(BORDER_ON)
        if self.presenter:
            self.presenter.on_generate(mode)

    def _make_mode_callback(self, mode: str) -> Callable[[], None]:
        return lambda: self._on_mode_click(mode)

    def _set_modes_state(self, state: str) -> None:
        """Habilita/deshabilita los clicks en las tarjetas de modo."""
        cursor = "hand2" if state == "normal" else "arrow"
        for card in self._mode_cards.values():
            card.inner().configure(cursor=cursor)
