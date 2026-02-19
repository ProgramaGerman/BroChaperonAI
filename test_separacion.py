"""
test_separacion.py — Script de prueba para la separación vocal.

Busca archivos de audio en la carpeta `test/`, procesa el primero que encuentre,
y muestra en consola el resultado detallado con tiempos.

Uso:
    uv run python test_separacion.py
"""

import sys
import time
from pathlib import Path

# Asegurar que el módulo logica sea importable desde la raíz del proyecto
RAIZ = Path(__file__).parent
sys.path.insert(0, str(RAIZ))

from logica.modelos import FormatosCompatibles
from logica.separador_audio import DemucsAudioSeparator


CARPETA_TEST = RAIZ / "test"
CARPETA_SALIDA = RAIZ / "test" / "output"


def buscar_archivo_test() -> Path | None:
    """Busca el primer archivo de audio compatible en la carpeta test/."""
    formatos = FormatosCompatibles()
    for archivo in sorted(CARPETA_TEST.iterdir()):
        if archivo.is_file() and formatos.es_audio(str(archivo)):
            return archivo
    return None


def main() -> None:
    print("=" * 60)
    print("  VOCAL REMOVER — Test de separación")
    print("=" * 60)

    if not CARPETA_TEST.exists():
        print(f"\n[ERROR] La carpeta '{CARPETA_TEST}' no existe.")
        print("Crea la carpeta 'test/' y coloca un archivo de audio dentro.")
        sys.exit(1)

    archivo = buscar_archivo_test()
    if archivo is None:
        formatos = FormatosCompatibles()
        extensiones = ", ".join(formatos.audio)
        print(f"\n[ERROR] No se encontró ningún archivo de audio en '{CARPETA_TEST}'.")
        print(f"Formatos soportados: {extensiones}")
        sys.exit(1)

    print(f"\n🎵 Archivo detectado : {archivo.name}")
    print(f"📁 Carpeta de salida : {CARPETA_SALIDA}")
    print("\n▶  Iniciando separación vocal...\n")

    separador = DemucsAudioSeparator()
    inicio = time.perf_counter()

    resultado = separador.separar(str(archivo), str(CARPETA_SALIDA))

    duracion = time.perf_counter() - inicio

    print()
    print("-" * 60)
    if resultado.exitoso:
        print(f"✅ ¡Éxito! ({duracion:.1f}s)")
        print(f"   Instrumental guardado en:\n   {resultado.ruta_salida}")
    else:
        print(f"❌ Error (después de {duracion:.1f}s):")
        print(f"\n{resultado.mensaje_error}")
    print("-" * 60)


if __name__ == "__main__":
    main()
