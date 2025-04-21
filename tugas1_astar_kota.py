import heapq
import math
import matplotlib.pyplot as plt
import networkx as nx

def euclidean(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# A* dengan bobot jalan
def a_star_weighted(cities, roads, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {city: float('inf') for city in cities}
    g_score[start] = 0

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor, weight in roads.get(current, []):
            tentative_g = g_score[current] + weight
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + euclidean(cities[neighbor], cities[goal])
                heapq.heappush(open_set, (f_score, neighbor))
    return []

# Data kota dan jalan dengan bobot (jarak/kondisi lalu lintas)
cities = {
    "A": (0, 0),
    "B": (2, 1),
    "C": (4, 2),
    "D": (5, 5),
    "E": (1, 4)
}

roads = {
    "A": [("B", 2.2), ("E", 4.0)],
    "B": [("A", 2.2), ("C", 2.0)],
    "C": [("B", 2.0), ("D", 3.2)],
    "D": [("C", 3.2)],
    "E": [("A", 4.0), ("D", 3.5)]
}

# Jalankan algoritma A*
path = a_star_weighted(cities, roads, "A", "D")
print("Rute terpendek dari A ke D (dengan bobot jalan):", path)

# Visualisasi graf dengan rute
G = nx.Graph()

# Tambahkan node dan posisi
for city, pos in cities.items():
    G.add_node(city, pos=pos)

# Tambahkan edge dengan bobot
for city, connections in roads.items():
    for neighbor, weight in connections:
        G.add_edge(city, neighbor, weight=weight)

# Gambar graf
pos = nx.get_node_attributes(G, 'pos')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=10)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Gambar jalur A* berwarna merah
if path:
    edge_path = list(zip(path[:-1], path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=edge_path, edge_color='red', width=2)

plt.title("Visualisasi Rute A* dari A ke D")
plt.show()
