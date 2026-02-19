"""
main.py — Punto de entrada de la aplicación Vocal Remover.
Bootstrap: crea el Presentador, la Vista y arranca el loop principal.
"""

from controlador.presentador import Presentador
from vista.ventana_principal import VentanaPrincipal


def main() -> None:
    presentador = Presentador()
    ventana = VentanaPrincipal(presentador)
    ventana.mainloop()


if __name__ == "__main__":
    main()
