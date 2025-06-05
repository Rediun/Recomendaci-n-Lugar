import heapq
from math import sqrt
import tkinter as tk

# Clase Lugar
class Lugar:
    def __init__(self, nombre, tipo, x, y, rating, reseñas):
        self.nombre = nombre
        self.tipo = tipo
        self.x = x
        self.y = y
        self.rating = rating
        self.reseñas = reseñas

    def distancia_a(self, otro):
        #usa pitagoras para calcular la distancia de cada nodo
        return sqrt((self.x - otro.x)**2 + (self.y - otro.y)**2)

    def rating_final(self):
        # Normaliza el rating con la cantidad de reseñas
        return self.rating * (1 + (self.reseñas / 100))

# Nodo inicial: el cliente
cliente = Lugar("Cliente", "Café", 2, 2, 0, 0)

# Lugares en el mapa (puedes meter más si quieres samuelito)
lugares = [
    Lugar("Café Aroma", "Café", 4.4, 1.7, 4.5, 200),
    Lugar("Museo Historia", "Museo", 5, 5, 4.8, 80),
    Lugar("Bar Noche", "Bar", 3, 4, 4.1, 150),
    Lugar("Hospital Bueno", "Hospital", 4, 1, 1, 150),
    Lugar("Llantera don chuy", "Llantera", 2, 3, 3, 150),
    Lugar("Café Sol", "Café", 2, 1, 4.2, 80),
    Lugar("Café Luna", "Café", 0.5, 0.5, 4.7, 100),
    Lugar("Tupulino", "Restaurante", 6, 2, 5, 300),
    Lugar("Tulio", "Tienda", 0.5, 2, 3, 80),
    Lugar("Oxxo", "Tienda", 3, 0.4, 1, 100),
    Lugar("Restaurante Rico", "Restaurante", 6, 4, 3.5, 300)
]

# Filtrar solo por tipo que busca el cliente
tipo_buscado = "Café"
candidatos = [lugar for lugar in lugares if lugar.tipo == tipo_buscado]

# Función A* para decidir mejor lugar (f = g + h)
def f(lugar):
    g = cliente.distancia_a(lugar)         # Distancia (costo real)
    h = -lugar.rating_final()              # Heurística: rating alto es mejor, por eso negativo
    return g + h

# Obtener mejor lugar según la función f
mejor_opcion = min(candidatos, key=f)

#intefaz graficona (no muy importante para la logica del proyectos)
class MapaGUI:
    def __init__(self, master):
        self.master = master
        master.title("Recomendador Interactivo de Lugares")

        self.canvas = tk.Canvas(master, width=500, height=500, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=2)

        self.label = tk.Label(master, text="", fg="green", font=("Arial", 12), justify="left")
        self.label.grid(row=1, column=0, columnspan=2, pady=10)

        # Menú desplegable
        self.tipo_var = tk.StringVar()
        self.tipo_var.set("Café")
        tipos = sorted(set(lugar.tipo for lugar in lugares))
        self.menu = tk.OptionMenu(master, self.tipo_var, *tipos, command=self.actualizar)
        self.menu.grid(row=2, column=0, pady=10)

        self.boton = tk.Button(master, text="Buscar Mejor Lugar", command=self.actualizar)
        self.boton.grid(row=2, column=1)

        self.actualizar()

    def escala(self, coord):
        return 60 + coord * 70

    def actualizar(self, *args):
        self.canvas.delete("all")
        tipo_buscado = self.tipo_var.get()
        candidatos = [lugar for lugar in lugares if lugar.tipo == tipo_buscado]

        if not candidatos:
            self.label.config(text="No hay lugares disponibles de ese tipo.")
            return

        def f(lugar):
            g = cliente.distancia_a(lugar)
            h = -lugar.rating_final()
            return g + h

        mejor = min(candidatos, key=f)

        cx, cy = self.escala(cliente.x), self.escala(cliente.y)
        self.canvas.create_oval(cx-7, cy-7, cx+7, cy+7, fill="blue")
        self.canvas.create_text(cx, cy-12, text="Cliente", fill="blue", font=("Arial", 10, "bold"))

        for lugar in lugares:
            x, y = self.escala(lugar.x), self.escala(lugar.y)
            color = "red" if lugar == mejor else "gray"
            self.canvas.create_oval(x-6, y-6, x+6, y+6, fill=color)
            self.canvas.create_text(x, y-12, text=lugar.nombre, fill=color)

            # Conectar con líneas
            line_color = "orange" if lugar == mejor else "#ccc"
            line_width = 3 if lugar == mejor else 1
            self.canvas.create_line(cx, cy, x, y, fill=line_color, width=line_width)

        # Mostrar info
        info = f"Lugar recomendado:\n➡ {mejor.nombre}\nDistancia: {cliente.distancia_a(mejor):.2f} unidades\n Rating ponderado: {mejor.rating_final():.2f}"
        self.label.config(text=info)

# Mostrar mapa
if __name__ == "__main__":
    root = tk.Tk()
    app = MapaGUI(root)
    root.mainloop()

# Mostrar resultado
print("Lugar recomendado:")
print(f"Nombre: {mejor_opcion.nombre}")
print(f"Distancia: {cliente.distancia_a(mejor_opcion):.2f} unidades")
print(f"Rating ponderado: {mejor_opcion.rating_final():.2f}")
