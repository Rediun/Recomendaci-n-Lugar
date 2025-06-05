import heapq
from math import sqrt

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
        return sqrt((self.x - otro.x)**2 + (self.y - otro.y)**2)

    def rating_final(self):
        # Normaliza el rating con la cantidad de reseñas
        return self.rating * (1 + (self.reseñas / 100))

# Nodo inicial: el cliente
cliente = Lugar("Cliente", "Café", 0, 0, 0, 0)

# Lugares en el mapa (puedes meter más si quieres)
lugares = [
    Lugar("Café Aroma", "Café", 1, 1, 4.5, 200),
    Lugar("Museo Historia", "Museo", 5, 5, 4.8, 80),
    Lugar("Bar Noche", "Bar", 3, 4, 4.1, 150),
    Lugar("Café Sol", "Café", 2, 1, 4.2, 80),
    Lugar("Café Luna", "Café", 0.5, 0.5, 4.7, 100),
    Lugar("Restaurante Rico", "Restaurante", 6, 1, 4.6, 300)
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

# Mostrar resultado
print("📍 Lugar recomendado:")
print(f"Nombre: {mejor_opcion.nombre}")
print(f"Distancia: {cliente.distancia_a(mejor_opcion):.2f} unidades")
print(f"Rating ponderado: {mejor_opcion.rating_final():.2f}")
