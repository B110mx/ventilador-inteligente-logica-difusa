import tkinter as tk
from tkinter import messagebox, Toplevel

# Importamos la lógica de cada compañero
from fuzzy_logic import calcular_velocidad
from data_validation import parse_temperature, TemperatureValidationError
import visualization

class VentiladorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ventilador Inteligente - Lógica Difusa")
        self.root.geometry("420x600")
        self.root.config(bg="#e8edf2")
        self.root.resizable(False, False)

        # Contenedor principal estilo tarjeta (Card)
        self.card = tk.Frame(root, bg="#ffffff", bd=0, highlightthickness=0)
        self.card.place(x=20, y=20, width=380, height=560)

        # Título principal moderno
        self.titulo_label = tk.Label(
            self.card, 
            text="Control Inteligente de Ventilador", 
            font=("Segoe UI", 13, "bold"),
            bg="#ffffff",
            fg="#1e293b"
        )
        self.titulo_label.pack(pady=(25, 15))

        # Marco para la entrada de temperatura
        self.frame_input = tk.Frame(self.card, bg="#ffffff")
        self.frame_input.pack(pady=10)

        self.label_temp = tk.Label(
            self.frame_input, 
            text="Ingrese la temperatura (°C):", 
            font=("Segoe UI", 11),
            bg="#ffffff",
            fg="#475569"
        )
        self.label_temp.pack(side=tk.LEFT, padx=5)

        self.entry_temp = tk.Entry(
            self.frame_input, 
            font=("Segoe UI", 11), 
            width=8,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#cbd5e1",
            highlightcolor="#3b82f6",
            justify="center"
        )
        self.entry_temp.pack(side=tk.LEFT, padx=5, ipady=3)

        # Botón moderno con estilo plano
        self.btn_calcular = tk.Button(
            self.card, 
            text="Calcular Velocidad", 
            font=("Segoe UI", 11, "bold"),
            bg="#3b82f6", 
            fg="white",
            activebackground="#2563eb",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.procesar_temperatura
        )
        self.btn_calcular.pack(pady=15)

        # Resultado de texto
        self.label_resultado = tk.Label(
            self.card, 
            text="Velocidad recomendada: --", 
            font=("Segoe UI", 11, "bold"),
            bg="#ffffff",
            fg="#0284c7"
        )
        self.label_resultado.pack(pady=5)

        # Canvas para el medidor semicircular (gauge)
        self.canvas_gauge = tk.Canvas(
            self.card, 
            width=260, 
            height=130, 
            bg="#ffffff", 
            highlightthickness=0
        )
        self.canvas_gauge.pack(pady=10)
        self.dibujar_gauge(0.0)

        # Botón para ver gráficas
        self.btn_graficas = tk.Button(
            self.card, 
            text="Ver Gráficas de Lógica Difusa", 
            font=("Segoe UI", 10),
            bg="#10b981", 
            fg="white",
            activebackground="#059669",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=5,
            command=self.mostrar_graficas
        )
        self.btn_graficas.pack(pady=20)
        self.btn_graficas["state"] = "disabled" # Se habilita tras un cálculo válido
        
        self.ultima_temperatura = None

    def dibujar_gauge(self, porcentaje):
        """Dibuja un medidor semicircular moderno que cambia de color según el valor."""
        self.canvas_gauge.delete("all")
        
        self.canvas_gauge.create_arc(
            20, 10, 240, 230, 
            start=0, extent=180, 
            style="arc", width=12, outline="#e2e8f0"
        )
        
        extent = (porcentaje / 100.0) * 180
        if extent > 0:
            if porcentaje < 40:
                color = "#0ea5e9"
            elif porcentaje < 75:
                color = "#10b981"
            else:
                color = "#ef4444"
            
            self.canvas_gauge.create_arc(
                20, 10, 240, 230, 
                start=180 - extent, extent=extent, 
                style="arc", width=12, outline=color
            )
        
        self.canvas_gauge.create_text(
            130, 85, 
            text=f"{porcentaje:.2f}%", 
            font=("Segoe UI", 15, "bold"), 
            fill="#1e293b"
        )

    def procesar_temperatura(self):
        temperatura_str = self.entry_temp.get().strip()
        
        try:
            # Validación utilizando la lógica de Luis Bryan
            temperatura = parse_temperature(temperatura_str)
            
            # Lógica difusa de Abril Miranda
            resultado_tuple = calcular_velocidad(temperatura)
            resultado_velocidad = resultado_tuple[0]
            
            # Interfaz de Mariana Córdova
            self.label_resultado.config(
                text=f"Velocidad recomendada: {resultado_velocidad:.2f}%"
            )
            self.dibujar_gauge(resultado_velocidad)
            
            self.ultima_temperatura = temperatura
            self.btn_graficas["state"] = "normal"
            
        except TemperatureValidationError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al calcular: {str(e)}")

    def mostrar_graficas(self):
        """Muestra las gráficas generadas por la lógica de Francesco Romero."""
        if self.ultima_temperatura is None:
            return
            
        ventana_graficas = Toplevel(self.root)
        ventana_graficas.title("Gráficas del Sistema Difuso")
        ventana_graficas.geometry("800x900")
        
        import matplotlib.pyplot as plt
        
        fig1 = plt.figure(figsize=(6, 3))
        fig2 = plt.figure(figsize=(6, 3))
        fig3 = plt.figure(figsize=(6, 3))
        
        visualization.grafica_pertenencia(self.ultima_temperatura, fig=fig1)
        visualization.grafica_activacion(self.ultima_temperatura, fig=fig2)
        visualization.grafica_respuesta(self.ultima_temperatura, fig=fig3)
        
        frame1 = tk.Frame(ventana_graficas)
        frame1.pack(fill="both", expand=True)
        visualization.embed_figure(fig1, frame1)
        
        frame2 = tk.Frame(ventana_graficas)
        frame2.pack(fill="both", expand=True)
        visualization.embed_figure(fig2, frame2)
        
        frame3 = tk.Frame(ventana_graficas)
        frame3.pack(fill="both", expand=True)
        visualization.embed_figure(fig3, frame3)

if __name__ == "__main__":
    root = tk.Tk()
    app = VentiladorApp(root)
    root.mainloop()
