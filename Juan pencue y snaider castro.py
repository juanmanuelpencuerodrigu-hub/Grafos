import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph(nombre="Red de Inspección Urbana", ciudad="Bogotá")
G.add_nodes_from(
    [
        ("Centro", {"tipo": "Hub Principal", "capacidad": 100}),
        ("Norte", {"tipo": "Residencial", "capacidad": 50}),
        ("Este", {"tipo": "Industrial", "capacidad": 80}),
        ("Sur", {"tipo": "Comercial", "capacidad": 60}),
        ("Oeste", {"tipo": "Residencial", "capacidad": 40}),
    ]
)
G.add_edges_from(
    [
        ("Centro", "Norte", {"distancia_km": 5, "nombre": "Av. Séptima"}),
        ("Norte", "Este", {"distancia_km": 3, "nombre": "Calle 100"}),
        ("Este", "Sur", {"distancia_km": 4, "nombre": "Av. Circunvalar"}),
        ("Sur", "Oeste", {"distancia_km": 6, "nombre": "Calle 26"}),
        ("Oeste", "Centro", {"distancia_km": 2, "nombre": "Av. Caracas"}),
        ("Norte", "Sur", {"distancia_km": 7, "nombre": "Diagonal Central"}),
    ]
)


def camino_hamilton(g, p=[]):
    if not p:
        return next((r for n in g if (r := camino_hamilton(g, [n]))), None)
    if len(p) == len(g):
        return p
    for vec in g[p[-1]]:
        if vec not in p and (r := camino_hamilton(g, p + [vec])):
            return r


nodos = list(G.nodes)
matriz = nx.to_numpy_array(G, weight=None, dtype=int)
ruta = camino_hamilton(G)

print(f"SISTEMA DE INSPECCIÓN - {G.graph['nombre'].upper()}\n")
print(
    "[1] MATRIZ DE ADYACENCIA\n          "
    + "".join(f"{n:>10}" for n in nodos)
)
for i, fila in enumerate(matriz):
    print(f"{nodos[i]:<10}" + "".join(f"{v:>10}" for v in fila))

print(
    "\n[2] DETALLE DE PUNTOS Y VÍAS\nDistritos:\n"
    + "\n".join(
        f"  • {k:<8} | Tipo: {v['tipo']:<14} | Capacidad: {v['capacidad']}"
        for k, v in G.nodes(data=True)
    )
)
print(
    "\nCalles:\n"
    + "\n".join(
        f"  • {u} ↔ {v:<8} | Vía: {d['nombre']:<16} | Distancia: {d['distancia_km']} km"
        for u, v, d in G.edges(data=True)
    )
)

print("\n[3] RUTA DE INSPECCIÓN ÓPTIMA (CAMINO DE HAMILTON)")
if ruta:
    print(
        "Secuencia:\n"
        + "\n".join(f"  Paso {i+1}: {nodo}" for i, nodo in enumerate(ruta))
    )
    print("\nTrayecto completo:\n  " + " ➔ ".join(ruta))

pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(9, 6))
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="lightblue",
    node_size=2500,
    font_weight="bold",
)

if ruta:
    aristas_ham = list(zip(ruta[:-1], ruta[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=aristas_ham, width=3.5, edge_color="r")

labels = {
    (u, v): f"{d['nombre']}\n({d['distancia_km']} km)"
    for u, v, d in G.edges(data=True)
}
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)
plt.title("Red Urbana - Camino de Hamilton (Rojo)")
plt.axis("off")
plt.tight_layout()
plt.savefig("grafo.png", dpi=300)
print("\nImagen guardada correctamente como 'grafo.png'")

try:
    plt.show()
except Exception:
    pass