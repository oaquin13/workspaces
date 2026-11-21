"""
reserva.py
==========
Clase Reserva: integra cliente, servicio, duración y estado.
Implementa confirmación, cancelación y procesamiento con manejo de
excepciones (try/except/else/finally y encadenamiento con "raise ... from").
"""

from datetime import datetime

from cliente import Cliente
from entidad_base import EntidadBase
from excepciones import (
    ErrorSoftwareFJ,
    OperacionNoPermitidaError,
    ReservaError,
    ServicioNoDisponibleError,
)
from registro import obtener_logger
from servicios import Servicio

log = obtener_logger()  # Logger compartido del sistema


class Reserva(EntidadBase):
    """Reserva de un servicio por parte de un cliente."""

    # Estados posibles de una reserva.
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    PROCESADA = "PROCESADA"
    CANCELADA = "CANCELADA"

    def __init__(self, cliente, servicio, duracion):
        # 1) Validamos los tipos de los objetos recibidos.
        if not isinstance(cliente, Cliente):
            raise ReservaError("La reserva requiere un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaError("La reserva requiere un servicio válido.")
        # 2) El servicio debe estar disponible.
        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre}' no está disponible."
            )
        # 3) Validamos la duración con las reglas propias del servicio.
        try:
            servicio.validar_parametros(duracion)
        except ErrorSoftwareFJ as causa:
            # Encadenamiento: el error original queda como "causa" del nuevo.
            raise ReservaError(
                f"Reserva incorrecta para '{servicio.nombre}': {causa.mensaje}"
            ) from causa
        # Si todo está bien, guardamos los datos (atributos privados).
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = self.PENDIENTE
        self.__costo_total = None  # Se calcula al procesar
        self.__creada = datetime.now()
        super().__init__("RES")  # ID al final: solo se gasta si la reserva es válida

    # ---------- Propiedades de solo lectura ----------
    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @property
    def servicio(self) -> Servicio:
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def costo_total(self):
        return self.__costo_total

    # ---------- Operaciones ----------
    def confirmar(self) -> None:
        """PENDIENTE -> CONFIRMADA."""
        if self.__estado != self.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar {self.id}: está {self.__estado}."
            )
        self.__estado = self.CONFIRMADA

    def cancelar(self) -> None:
        """Cancela si aún no fue procesada ni cancelada."""
        if self.__estado in (self.PROCESADA, self.CANCELADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar {self.id}: está {self.__estado}."
            )
        self.__estado = self.CANCELADA

    def procesar(self, impuesto=0.19, descuento=0.0) -> float:
        """CONFIRMADA -> PROCESADA, calculando el costo total."""
        if self.__estado != self.CONFIRMADA:
            raise OperacionNoPermitidaError(
                f"No se puede procesar {self.id}: debe estar CONFIRMADA y está {self.__estado}."
            )
        try:
            # Intentamos calcular el costo (puede fallar con datos inconsistentes).
            costo = self.__servicio.calcular_costo(self.__duracion, impuesto, descuento)
        except ErrorSoftwareFJ as causa:
            raise ReservaError(f"No se pudo procesar {self.id}: {causa.mensaje}") from causa
        else:
            # Solo se ejecuta si el try NO lanzó error: actualizamos el estado.
            self.__costo_total = costo
            self.__estado = self.PROCESADA
            return costo
        finally:
            # Se ejecuta SIEMPRE (haya error o no): dejamos huella en el log.
            log.debug("Intento de procesamiento de %s finalizado (estado: %s)",
                      self.id, self.__estado)

    def describir(self) -> str:
        costo = f"${self.__costo_total:,.2f}" if self.__costo_total is not None else "sin calcular"
        return (f"[{self.id}] {self.__cliente.nombre} -> {self.__servicio.nombre} | "
                f"duración: {self.__duracion} | {self.__estado} | costo: {costo}")
