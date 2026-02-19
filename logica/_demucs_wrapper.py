"""
_demucs_wrapper.py — Wrapper de Demucs que parchea torchaudio.load y torchaudio.save
con soundfile, evitando la dependencia de torchcodec en torchaudio >= 2.5 en Windows.
"""

import sys
import torch
import numpy as np
import soundfile as sf


def _aplicar_parche_torchaudio() -> None:
    """Reemplaza torchaudio.load y torchaudio.save por implementaciones con soundfile."""
    import torchaudio

    # ── Parche de CARGA ────────────────────────────────────────────────────────
    def _load_con_soundfile(
        uri,
        frame_offset: int = 0,
        num_frames: int = -1,
        normalize: bool = True,
        channels_first: bool = True,
        format=None,
        backend=None,
        encoding_config=None,
    ):
        data, sample_rate = sf.read(
            str(uri),
            start=frame_offset,
            frames=num_frames if num_frames > 0 else -1,
            always_2d=True,
            dtype="float32",
        )
        # soundfile: (frames, channels) → torch: (channels, frames)
        waveform = torch.from_numpy(data.T.copy())
        return waveform, sample_rate

    # ── Parche de GUARDADO ────────────────────────────────────────────────────
    def _save_con_soundfile(
        uri,
        src: torch.Tensor,
        sample_rate: int,
        channels_first: bool = True,
        compression=None,
        format: str | None = None,
        encoding: str | None = None,
        bits_per_sample: int | None = None,
        buffer_size: int = 4096,
        backend=None,
        encoding_config=None,
    ):
        # src shape: (channels, frames) → soundfile: (frames, channels)
        if channels_first:
            data = src.detach().cpu().numpy().T
        else:
            data = src.detach().cpu().numpy()

        ruta = str(uri)
        # soundfile necesita subtype para wav de 32 bits
        subtype = "FLOAT" if ruta.lower().endswith(".wav") else None
        sf.write(ruta, data, sample_rate, subtype=subtype)

    torchaudio.load = _load_con_soundfile
    torchaudio.save = _save_con_soundfile


if __name__ == "__main__":
    # Parchear ANTES de que demucs importe torchaudio internamente
    _aplicar_parche_torchaudio()

    from demucs.__main__ import main  # noqa: E402
    sys.exit(main())
