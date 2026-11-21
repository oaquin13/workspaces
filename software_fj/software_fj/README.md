# Software FJ – Sistema integral de gestión de clientes, servicios y reservas

Curso: Programación (213023) – UNAD – Ingeniería de Sistemas – Fase 4  
Lenguaje: Python 3.10 o superior (solo librerías estándar, sin base de datos).

## Cómo ejecutarlo
```bash
python main.py          # abre la consola interactiva (menú único)
python main.py --demo   # solo la simulación automática de 21 operaciones
```
La consola permite registrar clientes, crear servicios, manejar reservas y
visualizar todo (listados, panel general y registro de eventos). Los errores
y eventos quedan en `logs/eventos.log`.

## Estructura
| Archivo | Contenido |
|---|---|
| `excepciones.py` | Excepciones personalizadas (jerarquía desde `ErrorSoftwareFJ`) |
| `registro.py` | Configuración del archivo de logs |
| `entidad_base.py` | Clase abstracta `EntidadBase` (ID y descripción) |
| `cliente.py` | `Cliente` con validaciones y encapsulación |
| `servicios.py` | `Servicio` (abstracta) y `ReservaSala`, `AlquilerEquipo`, `Asesoria` |
| `reserva.py` | `Reserva` con confirmar, cancelar y procesar |
| `gestor.py` | `GestorFJ`: listas internas y ejecución protegida de operaciones |
| `consola.py` | Interfaz única de consola (menú interactivo y panel general) |
| `simulacion.py` | Simulación automática de 21 operaciones válidas e inválidas |
| `main.py` | Punto de entrada (`python main.py` o `python main.py --demo`) |

## Conceptos aplicados
- **Abstracción:** `EntidadBase` y `Servicio` son clases abstractas (`ABC`).
- **Herencia:** `Cliente`, `Servicio` y `Reserva` heredan de `EntidadBase`; los tres servicios heredan de `Servicio`.
- **Polimorfismo:** `calcular_costo`, `validar_parametros` y `describir` se sobrescriben en cada servicio.
- **Encapsulación:** atributos privados con propiedades y setters que validan.
- **Sobrecarga (simulada):** `calcular_costo(duracion, impuesto=0.0, descuento=0.0)` y `calcular_costo_con_iva(...)`.
- **Excepciones:** personalizadas, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from`.
- **Logs:** todo error y evento relevante queda en `logs/eventos.log`.
