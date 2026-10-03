import sys
import os

# Agregamos la carpeta src al PATH de Python para que pueda importar los módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import tkinter as tk
from interface import VentiladorApp

def main():
    print("Iniciando Sistema de Ventilador Inteligente...")
    root = tk.Tk()
    app = VentiladorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
