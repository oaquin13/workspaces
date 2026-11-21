"""
registro.py
===========
Configura el archivo de logs donde se guardan todos los eventos y errores.

El enunciado permite usar archivos ÚNICAMENTE para el registro de eventos
y errores, así que este es el único lugar donde el sistema escribe en disco.
"""

import logging  # Librería estándar de Python para registrar eventos
from pathlib import Path  # Para armar rutas que funcionen en cualquier sistema

# Carpeta "logs" junto a este archivo (no depende desde dónde se ejecute).
CARPETA_LOGS = Path(__file__).resolve().parent / "logs"
# Ruta completa del archivo de log.
ARCHIVO_LOG = CARPETA_LOGS / "eventos.log"


def obtener_logger() -> logging.Logger:
    """Devuelve el logger del sistema, creándolo la primera vez."""
    # Creamos la carpeta de logs si no existe (exist_ok evita error si ya existe).
    CARPETA_LOGS.mkdir(exist_ok=True)

    # Pedimos un logger con nombre propio; Python devuelve siempre el mismo.
    logger = logging.getLogger("software_fj")
    logger.setLevel(logging.DEBUG)  # Registramos desde el nivel más detallado

    # Si ya tiene manejadores no agregamos otro (evita líneas duplicadas).
    if not logger.handlers:
        # Manejador que escribe en el archivo (modo "a": agrega al final).
        manejador = logging.FileHandler(ARCHIVO_LOG, mode="a", encoding="utf-8")
        # Formato de cada línea: fecha, nivel, mensaje.
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        manejador.setFormatter(formato)  # Asociamos el formato al manejador
        logger.addHandler(manejador)  # Conectamos el manejador al logger

    return logger
