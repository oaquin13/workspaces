"""
entidad_base.py
===============
Clase abstracta que representa cualquier entidad general del sistema
(clientes, servicios y reservas). Aplica ABSTRACCIÓN y ENCAPSULACIÓN.
"""

from abc import ABC, abstractmethod  # ABC = Abstract Base Class


class EntidadBase(ABC):
    """Entidad general: todas tienen un identificador único y una descripción."""

    # Atributo de CLASE (compartido): un contador independiente por prefijo
    # (CLI, SAL, EQU, ASE, RES), así los IDs salen CLI-001, CLI-002, etc.
    _contadores = {}

    def __init__(self, prefijo: str):
        # Sumamos 1 al contador de este prefijo (empieza en 0 si no existe).
        numero = EntidadBase._contadores.get(prefijo, 0) + 1
        EntidadBase._contadores[prefijo] = numero
        # Atributo "privado" (encapsulado) con un ID legible, ej: CLI-001.
        self.__id = f"{prefijo}-{numero:03d}"

    @property
    def id(self) -> str:
        """Solo lectura: el ID no se puede modificar desde afuera."""
        return self.__id

    @abstractmethod
    def describir(self) -> str:
        """Cada entidad debe explicar cómo se describe (método abstracto)."""

    def __str__(self) -> str:
        # Al imprimir cualquier entidad se muestra su descripción.
        return self.describir()
