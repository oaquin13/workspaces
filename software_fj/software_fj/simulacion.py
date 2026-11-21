"""
simulacion.py
=============
Simulación automática de 21 operaciones (válidas e inválidas) para demostrar
que el sistema sigue funcionando aunque ocurran errores.

Usa su PROPIO gestor, así que no mezcla ni borra los datos que el usuario
haya registrado en la consola.
"""

from gestor import GestorFJ
from registro import ARCHIVO_LOG, obtener_logger


def titulo(numero: int, texto: str) -> None:
    """Imprime un encabezado para separar cada operación en pantalla."""
    print(f"\n--- Operación {numero}: {texto}")


def ejecutar_simulacion() -> None:
    log = obtener_logger()
    log.info("=" * 20 + " INICIO DE LA SIMULACIÓN " + "=" * 20)
    gestor = GestorFJ()

    print("=" * 70)
    print("SOFTWARE FJ - SIMULACIÓN DE OPERACIONES")
    print("=" * 70)

    # ------------------------- CLIENTES -------------------------
    titulo(1, "Registro VÁLIDO de cliente")
    ana = gestor.registrar_cliente("ana maría gómez", "1118456789", "ana.gomez@correo.com", "3105551234")

    titulo(2, "Registro VÁLIDO de cliente (sin teléfono, que es opcional)")
    carlos = gestor.registrar_cliente("Carlos Pérez", "94123456", "carlos.perez@correo.com")

    titulo(3, "Registro INVÁLIDO: correo mal escrito")
    gestor.registrar_cliente("Luis Rojas", "1020304050", "luis.rojas#correo")

    titulo(4, "Registro INVÁLIDO: documento con letras")
    gestor.registrar_cliente("María Torres", "12AB45", "maria@correo.com")

    titulo(5, "Registro INVÁLIDO: falta el correo (parámetro faltante)")
    gestor.registrar_cliente("Pedro Díaz", "55667788")

    titulo(6, "Registro INVÁLIDO: documento repetido")
    gestor.registrar_cliente("Ana Gómez Copia", "1118456789", "otra@correo.com")

    # ------------------------- SERVICIOS ------------------------
    titulo(7, "Creación VÁLIDA: sala de reuniones")
    sala = gestor.crear_servicio("sala", nombre="Sala Ejecutiva", tarifa_hora=50000, capacidad=12)

    titulo(8, "Creación VÁLIDA: alquiler de equipo")
    equipo = gestor.crear_servicio("equipo", nombre="Video Beam 4K", tarifa_dia=80000,
                                   equipo="Proyector", seguro=20000)

    titulo(9, "Creación VÁLIDA: asesoría especializada")
    asesoria = gestor.crear_servicio("asesoria", nombre="Asesoría en Ciberseguridad",
                                     tarifa_hora=120000, especialidad="Seguridad informática",
                                     nivel="senior")

    titulo(10, "Creación INVÁLIDA: tarifa negativa")
    gestor.crear_servicio("sala", nombre="Sala Fantasma", tarifa_hora=-5000, capacidad=4)

    titulo(11, "Creación INVÁLIDA: tipo de servicio que no existe")
    gestor.crear_servicio("hotel", nombre="Suite", tarifa_hora=300000)

    titulo(12, "Creación INVÁLIDA: faltan parámetros obligatorios")
    gestor.crear_servicio("equipo", nombre="Portátil")

    # ------------------------- RESERVAS -------------------------
    titulo(13, "Reserva VÁLIDA + confirmación + procesamiento con IVA")
    reserva1 = gestor.crear_reserva(ana.id, sala.id, 3)
    gestor.confirmar_reserva(reserva1.id)
    gestor.procesar_reserva(reserva1.id, impuesto=0.19)

    titulo(14, "Reserva VÁLIDA con descuento del 10 %")
    reserva2 = gestor.crear_reserva(carlos.id, equipo.id, 5)
    gestor.confirmar_reserva(reserva2.id)
    gestor.procesar_reserva(reserva2.id, impuesto=0.19, descuento=0.10)

    titulo(15, "Reserva INVÁLIDA: duración excede el máximo (20 horas en sala)")
    gestor.crear_reserva(ana.id, sala.id, 20)

    titulo(16, "Reserva INVÁLIDA: servicio no disponible")
    gestor.cambiar_disponibilidad(asesoria.id, False)
    gestor.crear_reserva(carlos.id, asesoria.id, 2)

    titulo(17, "Reserva INVÁLIDA: cliente que no existe")
    gestor.crear_reserva("CLI-999", sala.id, 2)

    titulo(18, "Operaciones NO PERMITIDAS por el estado de la reserva")
    reserva3 = gestor.crear_reserva(carlos.id, sala.id, 4)
    gestor.cancelar_reserva(reserva3.id)       # Se cancela bien
    gestor.confirmar_reserva(reserva3.id)      # Error: ya está cancelada
    gestor.procesar_reserva(reserva1.id)       # Error: ya fue procesada

    titulo(19, "Cálculo INCONSISTENTE: descuento del 150 %")
    reserva4 = gestor.crear_reserva(ana.id, equipo.id, 2)
    gestor.confirmar_reserva(reserva4.id)
    gestor.procesar_reserva(reserva4.id, descuento=1.5)

    titulo(20, "Error INESPERADO (división entre cero): el programa sigue")
    gestor._ejecutar("Cálculo de prueba", lambda: 1 / 0)

    titulo(21, "Después de tantos errores el sistema aún funciona: se reintenta bien")
    gestor.procesar_reserva(reserva4.id, descuento=0.05)

    # ------------------------- RESUMEN --------------------------
    gestor.resumen()
    log.info("=" * 20 + " FIN DE LA SIMULACIÓN " + "=" * 20)
    print(f"\nTodos los eventos y errores quedaron registrados en:\n  {ARCHIVO_LOG}")

