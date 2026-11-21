"""
gestor.py
=========
GestorFJ: administra las listas internas de clientes, servicios y reservas
(sin base de datos) y ejecuta cada operación de forma protegida para que
la aplicación NUNCA se detenga ante un error.
"""

from cliente import Cliente
from excepciones import (
    ErrorSoftwareFJ,
    ParametroFaltanteError,
    ReservaError,
    ServicioInvalidoError,
)
from registro import obtener_logger
from reserva import Reserva
from servicios import Asesoria, AlquilerEquipo, ReservaSala

log = obtener_logger()


class GestorFJ:
    """Punto central de la aplicación."""

    # Tipos de servicio que el gestor sabe crear.
    TIPOS_SERVICIO = {"sala": ReservaSala, "equipo": AlquilerEquipo, "asesoria": Asesoria}

    def __init__(self):
        # Listas internas: reemplazan a la base de datos.
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []
        # Contadores para el resumen final.
        self.exitosas = 0
        self.fallidas = 0

    # ------------------------------------------------------------------
    # Ejecutor protegido: aquí se concentra el manejo de excepciones
    # ------------------------------------------------------------------
    def _ejecutar(self, operacion: str, funcion, *args, **kwargs):
        """Ejecuta 'funcion' y captura cualquier error sin detener el programa."""
        try:
            resultado = funcion(*args, **kwargs)  # Intento de la operación
        except ErrorSoftwareFJ as error:
            # Error propio del sistema (dato inválido, estado no permitido, etc.).
            self.fallidas += 1
            log.error("%s FALLÓ -> %s: %s", operacion, type(error).__name__, error.mensaje)
            if error.__cause__ is not None:  # Si viene encadenado, registramos la causa
                log.error("    causa original: %s: %s",
                          type(error.__cause__).__name__, error.__cause__)
            print(f"   [ERROR CONTROLADO] {operacion}: {error.mensaje}")
            return None
        except Exception as error:  # noqa: BLE001  (error inesperado)
            # Cualquier otro error: lo registramos con el detalle completo.
            self.fallidas += 1
            log.critical("%s ERROR INESPERADO -> %s: %s", operacion,
                         type(error).__name__, error, exc_info=True)
            print(f"   [ERROR INESPERADO] {operacion}: {type(error).__name__}: {error}")
            return None
        else:
            # Solo si no hubo errores.
            self.exitosas += 1
            log.info("%s OK", operacion)
            return resultado
        finally:
            # Siempre se ejecuta.
            log.debug("Fin de la operación: %s", operacion)

    # ------------------------------------------------------------------
    # Búsquedas internas
    # ------------------------------------------------------------------
    def _buscar(self, lista, id_buscado, etiqueta):
        """Busca una entidad por ID en una lista; si no existe lanza error."""
        for elemento in lista:
            if elemento.id == id_buscado:
                return elemento
        raise ReservaError(f"No existe {etiqueta} con ID '{id_buscado}'.")

    # ------------------------------------------------------------------
    # Operaciones públicas (todas protegidas por _ejecutar)
    # ------------------------------------------------------------------
    def registrar_cliente(self, nombre=None, documento=None, email=None, telefono=None):
        def accion():
            # Documento único: no puede haber dos clientes con el mismo documento.
            cliente = Cliente(nombre, documento, email, telefono)
            if any(c.documento == cliente.documento for c in self.__clientes):
                raise ReservaError(f"Ya existe un cliente con documento {cliente.documento}.")
            self.__clientes.append(cliente)
            print(f"   Cliente registrado: {cliente}")
            return cliente
        return self._ejecutar("Registrar cliente", accion)

    def crear_servicio(self, tipo, **datos):
        def accion():
            clase = self.TIPOS_SERVICIO.get(str(tipo).lower())
            if clase is None:
                raise ServicioInvalidoError(
                    f"Tipo de servicio '{tipo}' no existe. Opciones: {', '.join(self.TIPOS_SERVICIO)}."
                )
            try:
                servicio = clase(**datos)
            except TypeError as causa:
                # Faltan o sobran parámetros en el constructor.
                raise ParametroFaltanteError(f"Parámetros incorrectos para '{tipo}': {causa}") from causa
            self.__servicios.append(servicio)
            print(f"   Servicio creado: {servicio}")
            return servicio
        return self._ejecutar(f"Crear servicio ({tipo})", accion)

    def crear_reserva(self, id_cliente, id_servicio, duracion):
        def accion():
            cliente = self._buscar(self.__clientes, id_cliente, "cliente")
            servicio = self._buscar(self.__servicios, id_servicio, "servicio")
            reserva = Reserva(cliente, servicio, duracion)
            self.__reservas.append(reserva)
            print(f"   Reserva creada: {reserva}")
            return reserva
        return self._ejecutar("Crear reserva", accion)

    def confirmar_reserva(self, id_reserva):
        def accion():
            reserva = self._buscar(self.__reservas, id_reserva, "reserva")
            reserva.confirmar()
            print(f"   Reserva confirmada: {reserva}")
            return reserva
        return self._ejecutar(f"Confirmar reserva {id_reserva}", accion)

    def cancelar_reserva(self, id_reserva):
        def accion():
            reserva = self._buscar(self.__reservas, id_reserva, "reserva")
            reserva.cancelar()
            print(f"   Reserva cancelada: {reserva}")
            return reserva
        return self._ejecutar(f"Cancelar reserva {id_reserva}", accion)

    def procesar_reserva(self, id_reserva, impuesto=0.19, descuento=0.0):
        def accion():
            reserva = self._buscar(self.__reservas, id_reserva, "reserva")
            reserva.procesar(impuesto, descuento)
            print(f"   Reserva procesada: {reserva}")
            return reserva
        return self._ejecutar(f"Procesar reserva {id_reserva}", accion)

    def cambiar_disponibilidad(self, id_servicio, estado):
        def accion():
            servicio = self._buscar(self.__servicios, id_servicio, "servicio")
            servicio.cambiar_disponibilidad(estado)
            print(f"   {servicio.id} disponible = {servicio.disponible}")
            return servicio
        return self._ejecutar(f"Cambiar disponibilidad {id_servicio}", accion)

    # ------------------------------------------------------------------
    # Consultas para la consola (devuelven COPIAS: la lista interna queda protegida)
    # ------------------------------------------------------------------
    def listar_clientes(self):
        return list(self.__clientes)

    def listar_servicios(self):
        return list(self.__servicios)

    def listar_reservas(self):
        return list(self.__reservas)

    # ------------------------------------------------------------------
    # Resumen
    # ------------------------------------------------------------------
    def resumen(self) -> None:
        print("\n" + "=" * 70)
        print("RESUMEN FINAL")
        print("=" * 70)
        print(f"Clientes registrados : {len(self.__clientes)}")
        print(f"Servicios creados    : {len(self.__servicios)}")
        print(f"Reservas             : {len(self.__reservas)}")
        print(f"Operaciones exitosas : {self.exitosas}")
        print(f"Operaciones fallidas : {self.fallidas}")
        print("\nReservas:")
        for reserva in self.__reservas:
            print(f"  {reserva}")
