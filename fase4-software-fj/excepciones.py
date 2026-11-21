"""
excepciones.py
==============
Jerarquía de excepciones personalizadas del sistema Software FJ.

Todas heredan de ErrorSoftwareFJ, así el gestor puede capturar
"cualquier error propio del sistema" con un solo bloque except.
"""


class ErrorSoftwareFJ(Exception):
    """Excepción base de todo el sistema (raíz de la jerarquía)."""

    def __init__(self, mensaje: str = "Error en Software FJ"):
        # Guardamos el mensaje en un atributo para poder leerlo después.
        self.mensaje = mensaje
        # Llamamos al constructor de Exception para que str(error) funcione.
        super().__init__(mensaje)


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando los datos de un cliente no cumplen las validaciones."""


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Se lanza cuando falta un dato obligatorio (None, vacío o ausente)."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando un servicio se crea o se configura con datos inválidos."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta reservar un servicio que no está disponible."""


class ReservaError(ErrorSoftwareFJ):
    """Se lanza cuando una reserva no se puede crear o procesar."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta una operación que el estado actual no permite."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se lanza cuando un cálculo de costos produce un resultado inválido."""
