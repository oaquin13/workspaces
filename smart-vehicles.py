import tkinter as tk
from tkinter import ttk


# ==========================================
# BASE CLASS: Vehiculo
# ==========================================
class Vehiculo:

  def __init__(self, marca, modelo, velocidad_actual=0):
    self.marca = marca
    self.modelo = modelo
    self.velocidad_actual = velocidad_actual

  # Método acelerar con sobrecarga simulada mediante parámetros opcionales
  def acelerar(self, turbo=False, terreno="normal"):
    incremento = 10  # Incremento base sin parámetros
    if turbo:
      incremento *= 2  # Con parámetro turbo opcional
    if terreno == "rough":
      incremento //= 2
    elif terreno == "slippery":
      incremento //= 3

    self.velocidad_actual += incremento
    return self.velocidad_actual

  def detener(self):
    self.velocidad_actual = 0
    return self.velocidad_actual

  def obtener_informacion(self):
    return (
        f"Brand: {self.marca} | Model: {self.modelo} | Speed:"
        f" {self.velocidad_actual} km/h"
    )


# ==========================================
# CHILD CLASSES (Polimorfismo y Herencia)
# ==========================================
class AutoElectrico(Vehiculo):

  def __init__(self, marca, modelo, bateria=100):
    super().__init__(marca, modelo)
    self.bateria = bateria

  def acelerar(self, turbo=False, terreno="normal"):
    # Acelera de forma progresiva y consume energía
    incremento = 15
    if turbo:
      incremento *= 1.8
      self.bateria -= 5
    self.bateria = max(0, self.bateria - 2)
    self.velocidad_actual += int(incremento)
    return self.velocidad_actual

  def detener(self):
    self.velocidad_actual = 0
    return f"Electric Car stopped with regenerative braking. Battery: {self.bateria}%"


class Moto(Vehiculo):

  def __init__(self, marca, modelo, estabilidad="High"):
    super().__init__(marca, modelo)
    self.estabilidad = estabilidad

  def acelerar(self, turbo=False, terreno="normal"):
    # Acelera rápidamente pero menor estabilidad
    incremento = 25
    if turbo:
      incremento *= 2.2
    if terreno == "slippery":
      self.estabilidad = "Low (Warning!)"
    else:
      self.estabilidad = "High"
    self.velocidad_actual += int(incremento)
    return self.velocidad_actual

  def detener(self):
    self.velocidad_actual = 0
    return "Motorcycle stopped sharply using ABS brakes."


class Camion(Vehiculo):

  def __init__(self, marca, modelo, peso_carga_ton=6):
    super().__init__(marca, modelo)
    self.peso_carga_ton = peso_carga_ton

  def acelerar(self, turbo=False, terreno="normal"):
    # Acelera lentamente debido a su mayor peso
    incremento = 8
    if turbo:
      incremento *= 1.2
    # El peso reduce la aceleración
    efectivo = max(2, int(incremento / (self.peso_carga_ton * 0.2)))
    self.velocidad_actual += efectivo
    return self.velocidad_actual

  def detener(self):
    self.velocidad_actual = 0
    return "Truck stopped slowly using air brakes."


# ==========================================
# GRAPHICAL USER INTERFACE (Tkinter - English)
# ==========================================
class SmartVehicleApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Smart Vehicles Simulation System")
    self.root.geometry("680x520")
    self.root.config(bg="#f4f4f9")

    # Lista de objetos de distintas clases (Polimorfismo)[cite: 2]
    self.vehicles = [
        AutoElectrico("Tesla", "Model S", 95),
        Moto("Yamaha", "MT-03", "High"),
        Camion("Volvo", "FH16", 8),
    ]

    # Título de la interfaz
    title_label = tk.Label(
        root,
        text="Smart Vehicles Polymorphism Simulation",
        font=("Arial", 14, "bold"),
        bg="#f4f4f9",
        fg="#333",
    )
    title_label.pack(pady=10)

    # Panel de controles
    control_frame = tk.LabelFrame(
        root,
        text=" Simulation Parameters ",
        font=("Arial", 10, "bold"),
        bg="#f4f4f9",
    )
    control_frame.pack(fill="both", expand="yes", padx=20, pady=10)

    # Checkbox para Turbo
    self.turbo_var = tk.BooleanVar()
    self.turbo_check = tk.Checkbutton(
        control_frame,
        text="Enable Turbo Mode",
        variable=self.turbo_var,
        bg="#f4f4f9",
        font=("Arial", 10),
    )
    self.turbo_check.grid(row=0, column=0, sticky="w", padx=15, pady=8)

    # Menú desplegable para Terreno
    tk.Label(
        control_frame,
        text="Terrain Condition:",
        bg="#f4f4f9",
        font=("Arial", 10),
    ).grid(row=0, column=1, sticky="w", padx=5, pady=8)
    self.terrain_cb = ttk.Combobox(
        control_frame, values=["normal", "rough", "slippery"], width=12, state="readonly"
    )
    self.terrain_cb.grid(row=0, column=2, padx=5, pady=8)
    self.terrain_cb.current(0)

    # Botón de acelerar usando un único ciclo (Polimorfismo)[cite: 2]
    self.btn_accelerate = tk.Button(
        control_frame,
        text="Accelerate All Vehicles (Polymorphism Loop)",
        command=self.simulate_acceleration,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=10,
        pady=5,
    )
    self.btn_accelerate.grid(
        row=1, column=0, columnspan=3, sticky="ew", padx=15, pady=10
    )

    # Botón de detener
    self.btn_stop = tk.Button(
        control_frame,
        text="Stop All Vehicles",
        command=self.simulate_stop,
        bg="#f44336",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=10,
        pady=5,
    )
    self.btn_stop.grid(
        row=2, column=0, columnspan=3, sticky="ew", padx=15, pady=5
    )

    # Área de registro de eventos (Log)
    log_frame = tk.LabelFrame(
        root, text=" System Activity Log ", font=("Arial", 10, "bold"), bg="#f4f4f9"
    )
    log_frame.pack(fill="both", expand="yes", padx=20, pady=10)

    self.text_log = tk.Text(log_frame, height=12, width=75, font=("Consolas", 9))
    self.text_log.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)

    scrollbar = tk.Scrollbar(log_frame, command=self.text_log.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    self.text_log.config(yscrollcommand=scrollbar.set)

    self.show_initial_status()

  def show_initial_status(self):
    self.text_log.insert(tk.END, "=== INITIAL VEHICLE FLEET STATUS ===\n")
    for v in self.vehicles:
      self.text_log.insert(tk.END, f"-> {v.obtener_informacion()}\n")
    self.text_log.insert(tk.END, "=" * 50 + "\n\n")

  def simulate_acceleration(self):
    turbo = self.turbo_var.get()
    terreno = self.terrain_cb.get()
    self.text_log.insert(
        tk.END,
        f"[TEST] Accelerating fleet | Turbo: {turbo} | Terrain: {terreno}\n",
    )

    # UNICO CICLO QUE DEMUESTRA POLIMORFISMO (Requisito de la guía)[cite: 2]
    for v in self.vehicles:
      v.acelerar(turbo=turbo, terreno=terreno)
      self.text_log.insert(tk.END, f"   * {v.obtener_informacion()}\n")

    self.text_log.insert(tk.END, "-" * 50 + "\n")
    self.text_log.see(tk.END)

  def simulate_stop(self):
    self.text_log.insert(
        tk.END, "[TEST] Stopping all vehicles simultaneously...\n"
    )

    # UNICO CICLO PARA DETENER USANDO POLIMORFISMO[cite: 2]
    for v in self.vehicles:
      msg = v.detener()
      self.text_log.insert(
          tk.END,
          f"   * {v.marca} {v.modelo} -> {msg} (Speed: {v.velocidad_actual}"
          " km/h)\n",
      )

    self.text_log.insert(tk.END, "-" * 50 + "\n")
    self.text_log.see(tk.END)


if __name__ == "__main__":
  root = tk.Tk()
  app = SmartVehicleApp(root)
  root.mainloop()