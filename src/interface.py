import tkinter as tk
from tkinter import messagebox

# Importamos la función de lógica difusa sin modificar tu archivo existente
from fuzzy_logic import calcular_velocidad

class VentiladorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ventilador Inteligente - Lógica Difusa")
        self.root.geometry("420x540")
        self.root.config(bg="#e8edf2")
        self.root.resizable(False, False)

        # Contenedor principal estilo tarjeta (Card)
        self.card = tk.Frame(root, bg="#ffffff", bd=0, highlightthickness=0)
        self.card.place(x=20, y=20, width=380, height=500)

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

    def dibujar_gauge(self, porcentaje):
        """Dibuja un medidor semicircular moderno que cambia de color según el valor."""
        self.canvas_gauge.delete("all")
        
        # Arco de fondo (gris claro)
        self.canvas_gauge.create_arc(
            20, 10, 240, 230, 
            start=0, extent=180, 
            style="arc", width=12, outline="#e2e8f0"
        )
        
        # Cálculo del ángulo del arco de valor
        extent = (porcentaje / 100.0) * 180
        if extent > 0:
            # Color dinámico (Azul para frío/medio, Rojo para alta velocidad)
            if porcentaje < 40:
                color = "#0ea5e9"  # Azul
            elif porcentaje < 75:
                color = "#10b981"  # Verde
            else:
                color = "#ef4444"  # Rojo
            
            self.canvas_gauge.create_arc(
                20, 10, 240, 230, 
                start=180 - extent, extent=extent, 
                style="arc", width=12, outline=color
            )
        
        # Texto del porcentaje en el centro del medidor
        self.canvas_gauge.create_text(
            130, 85, 
            text=f"{porcentaje:.2f}%", 
            font=("Segoe UI", 15, "bold"), 
            fill="#1e293b"
        )

    def procesar_temperatura(self):
        """Obtiene la temperatura de la interfaz, llama a la lógica difusa y muestra el resultado."""
        temperatura_str = self.entry_temp.get().strip()
        
        if not temperatura_str:
            messagebox.showerror("Error", "Por favor ingrese un valor de temperatura.")
            return

        try:
            # Convertimos el texto ingresado a un valor flotante
            temperatura = float(temperatura_str)
            
            # Llamamos a la función calcular_velocidad de tu módulo fuzzy_logic
            resultado_tuple = calcular_velocidad(temperatura)
            resultado_velocidad = resultado_tuple[0]
            
            # Actualizamos texto y medidor gráfico
            self.label_resultado.config(
                text=f"Velocidad recomendada: {resultado_velocidad:.2f}%"
            )
            self.dibujar_gauge(resultado_velocidad)
            
        except ValueError:
            messagebox.showerror("Error de formato", "Ingrese un número válido para la temperatura.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al calcular: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VentiladorApp(root)
    root.mainloop()