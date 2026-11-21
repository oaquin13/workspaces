"""
servicios.py
============
Clase abstracta Servicio y tres servicios especializados:
    - ReservaSala     (reserva de salas)
    - AlquilerEquipo  (alquiler de equipos)
    - Asesoria        (asesorías especializadas)

Aplica HERENCIA, POLIMORFISMO (métodos sobrescritos) y SOBRECARGA.
Nota: Python no tiene sobrecarga real como Java; se simula con parámetros
opcionales y con métodos variantes (ver calcular_costo y calcular_costo_con_iva).
"""

import math  # Para comprobar que los números sean finitos (no nan ni inf)
from abc import abstractmethod

from entidad_base import EntidadBase
from excepciones import (
    CalculoInconsistenteError,
    ParametroFaltanteError,
    ServicioInvalidoError,
)

# IVA de Colombia usado en la variante calcular_costo_con_iva.
IVA = 0.19


class Servicio(EntidadBase):
    """Servicio general. Es abstracta: no se puede instanciar directamente."""

    def __init__(self, prefijo: str, nombre, tarifa_base, disponible: bool = True):
        # Validamos nombre y tarifa antes de guardarlos.
        if nombre is None or str(nombre).strip() == "":
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        # bool es subclase de int, por eso lo excluimos explícitamente.
        if isinstance(tarifa_base, bool) or not isinstance(tarifa_base, (int, float)):
            raise ServicioInvalidoError(f"La tarifa debe ser numérica: {tarifa_base!r}")
        if not math.isfinite(tarifa_base) or tarifa_base <= 0:
            raise ServicioInvalidoError(f"La tarifa debe ser un número mayor a 0: {tarifa_base}")
        self._nombre = str(nombre).strip()  # Protegido: lo usan las subclases
        self._tarifa_base = float(tarifa_base)
        self.__disponible = bool(disponible)  # Privado: solo con el método
        super().__init__(prefijo)  # El ID se genera al final, solo si todo es válido

    # ---------- Propiedades de solo lectura ----------
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self.__disponible

    def cambiar_disponibilidad(self, estado: bool) -> None:
        """Único punto de entrada para activar/desactivar el servicio."""
        self.__disponible = bool(estado)

    # ---------- Métodos abstractos (cada hijo los sobrescribe) ----------
    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0) -> float:
        """Calcula el costo. 'impuesto' y 'descuento' son opcionales (sobrecarga)."""

    @abstractmethod
    def validar_parametros(self, duracion) -> None:
        """Valida la duración según las reglas propias de cada servicio."""

    # ---------- Variante sobrecargada ----------
    def calcular_costo_con_iva(self, duracion, descuento=0.0) -> float:
        """Variante: costo con el IVA colombiano ya aplicado."""
        return self.calcular_costo(duracion, impuesto=IVA, descuento=descuento)

    # ---------- Utilidad compartida por los hijos ----------
    @staticmethod
    def _aplicar_ajustes(subtotal: float, impuesto: float, descuento: float) -> float:
        """Aplica descuento e impuesto validando que los porcentajes sean lógicos."""
        # Los porcentajes deben ser números entre 0 y 1 (0 % a 100 %).
        for etiqueta, valor in (("impuesto", impuesto), ("descuento", descuento)):
            if isinstance(valor, bool) or not isinstance(valor, (int, float)):
                raise CalculoInconsistenteError(f"El {etiqueta} debe ser numérico: {valor!r}")
            if not 0 <= valor <= 1:
                raise CalculoInconsistenteError(
                    f"El {etiqueta} debe estar entre 0 y 1 (recibido {valor})."
                )
        # Primero se descuenta y luego se suma el impuesto.
        total = subtotal * (1 - descuento) * (1 + impuesto)
        if total <= 0:
            raise CalculoInconsistenteError(f"El costo calculado no es válido: {total}")
        return round(total, 2)

    @staticmethod
    def _numero_positivo(valor, nombre: str, maximo: float) -> float:
        """Valida que 'valor' sea un número mayor que 0 y no supere 'maximo'."""
        if valor is None:
            raise ParametroFaltanteError(f"Falta el parámetro '{nombre}'.")
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ServicioInvalidoError(f"'{nombre}' debe ser numérico: {valor!r}")
        if not 0 < valor <= maximo:
            raise ServicioInvalidoError(
                f"'{nombre}' debe ser mayor a 0 y máximo {maximo}: recibido {valor}."
            )
        return valor


class ReservaSala(Servicio):
    """Reserva de salas: se cobra por hora (máximo 12 horas)."""

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        # Validamos lo propio de la sala antes de generar el ID.
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad < 1:
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}")
        self.__capacidad = capacidad
        super().__init__("SAL", nombre, tarifa_hora, disponible)

    def validar_parametros(self, duracion) -> None:
        self._numero_positivo(duracion, "horas", 12)

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0) -> float:
        self.validar_parametros(duracion)  # Primero validamos
        subtotal = self.tarifa_base * duracion  # tarifa por hora * horas
        return self._aplicar_ajustes(subtotal, impuesto, descuento)

    def describir(self) -> str:
        return (f"[{self.id}] Sala '{self.nombre}' | capacidad {self.__capacidad} "
                f"personas | ${self.tarifa_base:,.0f} por hora")


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: se cobra por día (máximo 30) más un seguro fijo."""

    def __init__(self, nombre, tarifa_dia, equipo, seguro=0.0, disponible=True):
        if equipo is None or str(equipo).strip() == "":
            raise ParametroFaltanteError("Debe indicar el equipo a alquilar.")
        if isinstance(seguro, bool) or not isinstance(seguro, (int, float)) or not math.isfinite(seguro) or seguro < 0:
            raise ServicioInvalidoError(f"Seguro inválido: {seguro!r}")
        self.__equipo = str(equipo).strip()
        self.__seguro = float(seguro)
        super().__init__("EQU", nombre, tarifa_dia, disponible)

    def validar_parametros(self, duracion) -> None:
        self._numero_positivo(duracion, "días", 30)
        if int(duracion) != duracion:  # Los días deben ser enteros
            raise ServicioInvalidoError(f"Los días deben ser enteros: {duracion}")

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0) -> float:
        self.validar_parametros(duracion)
        subtotal = self.tarifa_base * duracion + self.__seguro  # días + seguro
        return self._aplicar_ajustes(subtotal, impuesto, descuento)

    def describir(self) -> str:
        return (f"[{self.id}] Equipo '{self.__equipo}' ({self.nombre}) | "
                f"${self.tarifa_base:,.0f} por día + seguro ${self.__seguro:,.0f}")


class Asesoria(Servicio):
    """Asesoría especializada: por hora (máximo 8), con recargo según el nivel."""

    # Multiplicador de la tarifa según el nivel del asesor.
    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, nombre, tarifa_hora, especialidad, nivel="junior", disponible=True):
        if especialidad is None or str(especialidad).strip() == "":
            raise ParametroFaltanteError("Debe indicar la especialidad.")
        nivel = str(nivel).strip().lower()
        if nivel not in self.NIVELES:
            raise ServicioInvalidoError(
                f"Nivel '{nivel}' no válido. Opciones: {', '.join(self.NIVELES)}."
            )
        self.__especialidad = str(especialidad).strip()
        self.__nivel = nivel
        super().__init__("ASE", nombre, tarifa_hora, disponible)

    def validar_parametros(self, duracion) -> None:
        self._numero_positivo(duracion, "horas", 8)

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0) -> float:
        self.validar_parametros(duracion)
        subtotal = self.tarifa_base * self.NIVELES[self.__nivel] * duracion
        return self._aplicar_ajustes(subtotal, impuesto, descuento)

    def describir(self) -> str:
        return (f"[{self.id}] Asesoría '{self.nombre}' en {self.__especialidad} | "
                f"nivel {self.__nivel} | ${self.tarifa_base:,.0f} por hora base")
