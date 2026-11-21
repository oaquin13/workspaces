"""
consola.py
==========
Interfaz única de consola de Software FJ.

Desde este menú se registran clientes, se crean servicios, se manejan las
reservas y se visualiza todo el sistema (listados, panel general y log).
Ningún dato mal escrito detiene el programa: todo pasa por el gestor, que
captura y registra los errores.
"""

from gestor import GestorFJ
from registro import ARCHIVO_LOG, obtener_logger
from reserva import Reserva
from simulacion import ejecutar_simulacion

log = obtener_logger()
ANCHO = 74  # Ancho de las líneas decorativas


def linea(caracter: str = "=") -> None:
    """Imprime una línea decorativa."""
    print(caracter * ANCHO)


def convertir(texto):
    """Convierte el texto a int o float si es posible.

    Si no es un número devuelve el texto tal cual: el sistema lo rechazará
    con su propia validación y quedará registrado en el log.
    """
    if texto is None:
        return None
    try:
        return int(texto)  # Primero intentamos entero (ej: 3)
    except ValueError:
        pass
    try:
        return float(texto.replace(",", "."))  # Luego decimal (ej: 0,19 o 0.19)
    except ValueError:
        return texto


class ConsolaFJ:
    """Menú interactivo de la aplicación."""

    def __init__(self):
        self.gestor = GestorFJ()  # Gestor con los datos reales del usuario

    # ------------------------------------------------------------------
    # Utilidades de entrada
    # ------------------------------------------------------------------
    @staticmethod
    def pedir(mensaje: str):
        """Pide un dato por teclado. Devuelve None si el usuario deja vacío."""
        texto = input(f"   {mensaje}: ").strip()
        return texto if texto else None

    @staticmethod
    def pedir_id(mensaje: str):
        """Pide un ID y lo normaliza (mayúsculas, sin espacios)."""
        texto = input(f"   {mensaje}: ").strip().upper()
        return texto if texto else None

    @staticmethod
    def pausa() -> None:
        """Espera Enter para que el usuario alcance a leer la pantalla."""
        try:
            input("\n   Presiona Enter para volver al menú...")
        except EOFError:  # Si no hay teclado (entrada cerrada) seguimos
            pass

    # ------------------------------------------------------------------
    # Menú
    # ------------------------------------------------------------------
    def mostrar_menu(self) -> None:
        print()
        linea()
        print("  SOFTWARE FJ - Gestión de clientes, servicios y reservas")
        linea()
        print("  CLIENTES                      SERVICIOS")
        print("   1. Registrar cliente          3. Crear servicio")
        print("   2. Ver clientes               4. Ver servicios")
        print("                                 5. Activar / desactivar servicio")
        print("  RESERVAS                      SISTEMA")
        print("   6. Crear reserva             11. Panel general")
        print("   7. Confirmar reserva         12. Ver registro de eventos (log)")
        print("   8. Cancelar reserva          13. Cargar datos de ejemplo")
        print("   9. Procesar reserva (costo)  14. Simulación automática")
        print("  10. Ver reservas               0. Salir")
        linea("-")

    def ejecutar(self) -> None:
        """Bucle principal: muestra el menú hasta que el usuario elija salir."""
        acciones = {
            "1": self.registrar_cliente, "2": self.ver_clientes,
            "3": self.crear_servicio, "4": self.ver_servicios,
            "5": self.cambiar_disponibilidad,
            "6": self.crear_reserva, "7": self.confirmar_reserva,
            "8": self.cancelar_reserva, "9": self.procesar_reserva,
            "10": self.ver_reservas, "11": self.panel_general,
            "12": self.ver_log, "13": self.cargar_ejemplos,
            "14": self.simulacion,
        }
        log.info("Consola iniciada")
        try:
            while True:
                self.mostrar_menu()
                opcion = input("  Elige una opción: ").strip()
                if opcion == "0":
                    break
                accion = acciones.get(opcion)
                if accion is None:
                    print(f"\n   Opción '{opcion}' no válida. Elige un número del menú.")
                    log.warning("Opción de menú inválida: %r", opcion)
                    continue
                print()
                try:
                    accion()
                except KeyboardInterrupt:
                    print("\n   Operación cancelada.")
                except Exception as error:  # noqa: BLE001  (última red de seguridad)
                    log.critical("Error inesperado en la consola: %s", error, exc_info=True)
                    print(f"   [ERROR INESPERADO] {type(error).__name__}: {error}")
        except (EOFError, KeyboardInterrupt):
            print()  # Salto de línea limpio si cierran la entrada con Ctrl+C / Ctrl+D
        log.info("Consola finalizada")
        print("\n   Gracias por usar Software FJ. ¡Hasta pronto!\n")

    # ------------------------------------------------------------------
    # Clientes
    # ------------------------------------------------------------------
    def registrar_cliente(self) -> None:
        print("  REGISTRAR CLIENTE")
        nombre = self.pedir("Nombre completo")
        documento = self.pedir("Documento (solo números)")
        email = self.pedir("Correo electrónico")
        telefono = self.pedir("Teléfono (opcional, Enter para omitir)")
        self.gestor.registrar_cliente(nombre, documento, email, telefono)
        self.pausa()

    def ver_clientes(self) -> None:
        print("  CLIENTES REGISTRADOS")
        clientes = self.gestor.listar_clientes()
        if not clientes:
            print("   (no hay clientes registrados)")
        for cliente in clientes:
            print(f"   {cliente}")
        self.pausa()

    # ------------------------------------------------------------------
    # Servicios
    # ------------------------------------------------------------------
    def crear_servicio(self) -> None:
        print("  CREAR SERVICIO")
        print("   1. Reserva de sala   2. Alquiler de equipo   3. Asesoría")
        tipo = self.pedir("Tipo de servicio (1-3)")
        nombre = self.pedir("Nombre del servicio")
        if tipo == "1":
            tarifa = convertir(self.pedir("Tarifa por hora ($)"))
            capacidad = convertir(self.pedir("Capacidad (personas)"))
            self.gestor.crear_servicio("sala", nombre=nombre, tarifa_hora=tarifa,
                                       capacidad=capacidad)
        elif tipo == "2":
            tarifa = convertir(self.pedir("Tarifa por día ($)"))
            equipo = self.pedir("Equipo a alquilar")
            seguro = convertir(self.pedir("Seguro fijo ($, Enter = 0)")) or 0
            self.gestor.crear_servicio("equipo", nombre=nombre, tarifa_dia=tarifa,
                                       equipo=equipo, seguro=seguro)
        elif tipo == "3":
            tarifa = convertir(self.pedir("Tarifa base por hora ($)"))
            especialidad = self.pedir("Especialidad")
            nivel = self.pedir("Nivel (junior / senior / experto, Enter = junior)") or "junior"
            self.gestor.crear_servicio("asesoria", nombre=nombre, tarifa_hora=tarifa,
                                       especialidad=especialidad, nivel=nivel)
        else:
            # Tipo desconocido: el gestor lo rechaza y lo registra en el log.
            self.gestor.crear_servicio(tipo or "")
        self.pausa()

    def ver_servicios(self) -> None:
        print("  SERVICIOS")
        servicios = self.gestor.listar_servicios()
        if not servicios:
            print("   (no hay servicios creados)")
        for servicio in servicios:
            estado = "disponible" if servicio.disponible else "NO disponible"
            print(f"   {servicio}  -> {estado}")
        self.pausa()

    def cambiar_disponibilidad(self) -> None:
        print("  ACTIVAR / DESACTIVAR SERVICIO")
        for servicio in self.gestor.listar_servicios():
            estado = "disponible" if servicio.disponible else "NO disponible"
            print(f"   {servicio.id} - {servicio.nombre} ({estado})")
        id_servicio = self.pedir_id("ID del servicio")
        accion = self.pedir("¿Activar (s) o desactivar (n)?")
        self.gestor.cambiar_disponibilidad(id_servicio, (accion or "").lower() == "s")
        self.pausa()

    # ------------------------------------------------------------------
    # Reservas
    # ------------------------------------------------------------------
    def crear_reserva(self) -> None:
        print("  CREAR RESERVA")
        for cliente in self.gestor.listar_clientes():
            print(f"   {cliente.id} - {cliente.nombre}")
        id_cliente = self.pedir_id("ID del cliente")
        for servicio in self.gestor.listar_servicios():
            print(f"   {servicio.id} - {servicio.nombre}")
        id_servicio = self.pedir_id("ID del servicio")
        duracion = convertir(self.pedir("Duración (horas para salas/asesorías, días para equipos)"))
        self.gestor.crear_reserva(id_cliente, id_servicio, duracion)
        self.pausa()

    def _mostrar_reservas_en_estado(self, estados) -> None:
        """Muestra solo las reservas cuyo estado esté en 'estados'."""
        for reserva in self.gestor.listar_reservas():
            if reserva.estado in estados:
                print(f"   {reserva}")

    def confirmar_reserva(self) -> None:
        print("  CONFIRMAR RESERVA (solo reservas PENDIENTES)")
        self._mostrar_reservas_en_estado((Reserva.PENDIENTE,))
        self.gestor.confirmar_reserva(self.pedir_id("ID de la reserva"))
        self.pausa()

    def cancelar_reserva(self) -> None:
        print("  CANCELAR RESERVA (PENDIENTES o CONFIRMADAS)")
        self._mostrar_reservas_en_estado((Reserva.PENDIENTE, Reserva.CONFIRMADA))
        self.gestor.cancelar_reserva(self.pedir_id("ID de la reserva"))
        self.pausa()

    def procesar_reserva(self) -> None:
        print("  PROCESAR RESERVA (solo reservas CONFIRMADAS)")
        self._mostrar_reservas_en_estado((Reserva.CONFIRMADA,))
        id_reserva = self.pedir_id("ID de la reserva")
        impuesto = convertir(self.pedir("Impuesto (ej. 0.19, Enter = 0.19)"))
        descuento = convertir(self.pedir("Descuento (ej. 0.10, Enter = 0)"))
        self.gestor.procesar_reserva(
            id_reserva,
            0.19 if impuesto is None else impuesto,
            0.0 if descuento is None else descuento,
        )
        self.pausa()

    def ver_reservas(self) -> None:
        print("  RESERVAS")
        reservas = self.gestor.listar_reservas()
        if not reservas:
            print("   (no hay reservas)")
        for reserva in reservas:
            print(f"   {reserva}")
        self.pausa()

    # ------------------------------------------------------------------
    # Sistema
    # ------------------------------------------------------------------
    def panel_general(self) -> None:
        """Vista resumida de todo el sistema."""
        clientes = self.gestor.listar_clientes()
        servicios = self.gestor.listar_servicios()
        reservas = self.gestor.listar_reservas()
        facturado = sum(r.costo_total for r in reservas if r.costo_total is not None)

        linea()
        print("  PANEL GENERAL")
        linea()
        print(f"   Clientes registrados : {len(clientes)}")
        print(f"   Servicios            : {len(servicios)} "
              f"({sum(1 for s in servicios if s.disponible)} disponibles)")
        print(f"   Reservas             : {len(reservas)}")
        for estado in (Reserva.PENDIENTE, Reserva.CONFIRMADA, Reserva.PROCESADA, Reserva.CANCELADA):
            cantidad = sum(1 for r in reservas if r.estado == estado)
            print(f"      - {estado:<10}: {cantidad}")
        print(f"   Total facturado      : ${facturado:,.2f}")
        print(f"   Operaciones exitosas : {self.gestor.exitosas}")
        print(f"   Operaciones fallidas : {self.gestor.fallidas}")
        linea("-")
        self.ver_log(ultimas=5, con_pausa=False)
        self.pausa()

    def ver_log(self, ultimas: int = 15, con_pausa: bool = True) -> None:
        """Muestra las últimas líneas importantes del archivo de log."""
        print(f"  ÚLTIMOS EVENTOS DEL REGISTRO ({ARCHIVO_LOG.name})")
        if not ARCHIVO_LOG.exists():
            print("   (el registro aún no existe)")
        else:
            lineas = ARCHIVO_LOG.read_text(encoding="utf-8").splitlines()
            # Ocultamos el nivel DEBUG para que la lectura sea más clara.
            importantes = [l for l in lineas if "| DEBUG" not in l]
            for texto in importantes[-ultimas:]:
                print(f"   {texto}")
        if con_pausa:
            self.pausa()

    def cargar_ejemplos(self) -> None:
        print("  CARGANDO DATOS DE EJEMPLO...")
        self.gestor.registrar_cliente("Ana María Gómez", "1118456789", "ana.gomez@correo.com", "3105551234")
        self.gestor.registrar_cliente("Carlos Pérez", "94123456", "carlos.perez@correo.com")
        self.gestor.crear_servicio("sala", nombre="Sala Ejecutiva", tarifa_hora=50000, capacidad=12)
        self.gestor.crear_servicio("equipo", nombre="Video Beam 4K", tarifa_dia=80000,
                                   equipo="Proyector", seguro=20000)
        self.gestor.crear_servicio("asesoria", nombre="Asesoría en Ciberseguridad",
                                   tarifa_hora=120000, especialidad="Seguridad informática",
                                   nivel="senior")
        self.pausa()

    def simulacion(self) -> None:
        print("  SIMULACIÓN AUTOMÁTICA (no modifica tus datos de la consola)")
        ejecutar_simulacion()
        self.pausa()
