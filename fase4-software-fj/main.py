"""
main.py
=======
Software FJ - Sistema integral de gestión de clientes, servicios y reservas.
Programación (213023) - UNAD - Fase 4.

Uso:
    python main.py          -> abre la consola interactiva (menú único)
    python main.py --demo   -> ejecuta solo la simulación automática y termina
"""

import sys

from consola import ConsolaFJ
from simulacion import ejecutar_simulacion


def main() -> None:
    # Si se pasa --demo se corre la simulación sin abrir el menú.
    if "--demo" in sys.argv[1:]:
        ejecutar_simulacion()
    else:
        ConsolaFJ().ejecutar()


if __name__ == "__main__":
    main()
