import networkx as nx

G = nx.Graph(nombre="Red de Inspección Urbana", ciudad="Bogotá")

nodos_con_atributos = [
    ("Centro", {"tipo": "Hub Principal", "capacidad": 100}),
    ("Norte", {"tipo": "Residencial", "capacidad": 50}),
    ("Este", {"tipo": "Industrial", "capacidad": 80}),
    ("Sur", {"tipo": "Comercial", "capacidad": 60}),
    ("Oeste", {"tipo": "Residencial", "capacidad": 40}),
]
G.add_nodes_from(nodos_con_atributos)

calles_con_atributos = [
    ("Centro", "Norte", {"distancia_km": 5, "nombre": "Av. Séptima"}),
    ("Norte", "Este", {"distancia_km": 3, "nombre": "Calle 100"}),
    ("Este", "Sur", {"distancia_km": 4, "nombre": "Av. Circunvalar"}),
    ("Sur", "Oeste", {"distancia_km": 6, "nombre": "Calle 26"}),
    ("Oeste", "Centro", {"distancia_km": 2, "nombre": "Av. Caracas"}),
    ("Norte", "Sur", {"distancia_km": 7, "nombre": "Diagonal Central"}),
]
G.add_edges_from(calles_con_atributos)


def obtener_camino_hamilton(grafo):
    lista_nodos = list(grafo.nodes())
    total_nodos = len(lista_nodos)
    camino = []

    def resolver(nodo_actual):
        camino.append(nodo_actual)
        if len(camino) == total_nodos:
            return True

        for vecino in grafo.neighbors(nodo_actual):
            if vecino not in camino:
                if resolver(vecino):
                    return True

        camino.pop()
        return False

    for inicio in lista_nodos:
        if resolver(inicio):
            return camino
    return None


if __name__ == "__main__":
    lista_nodos = list(G.nodes())
    matriz = nx.to_numpy_array(G, weight=None, dtype=int)

    print(f"    SISTEMA DE INSPECCIÓN - {G.graph['nombre'].upper()}")

    print("\n[1] MATRIZ DE ADYACENCIA")
    encabezado = f"{'':10}" + "".join([f"{nodo:>10}" for nodo in lista_nodos])
    print(encabezado)
    for i, fila in enumerate(matriz):
        fila_str = "".join([f"{val:>10}" for val in fila])
        print(f"{lista_nodos[i]:<10}{fila_str}")

    print("\n[2] DETALLE DE PUNTOS Y VÍAS REGISTRADAS")
    print("Distritos (Nodos):")
    for nodo, attr in G.nodes(data=True):
        print(
            f"  • {nodo:<8} | Tipo: {attr['tipo']:<14} | Capacidad: {attr['capacidad']}"
        )

    print("\nCalles (Aristas):")
    for u, v, attr in G.edges(data=True):
        print(
            f"  • {u} ↔ {v:<8} | Vía: {attr['nombre']:<16} | Distancia: {attr['distancia_km']} km"
        )

    print("\n[3] RUTA DE INSPECCIÓN ÓPTIMA (CAMINO DE HAMILTON)")
    ruta = obtener_camino_hamilton(G)

    if ruta:
        print("Objetivo: Visitar cada distrito exactamente una vez.\n")
        print("Secuencia de visita:")
        for paso, distrito in enumerate(ruta, 1):
            print(f"  Paso {paso}: {distrito}")

        print("\nTrayecto completo:")
        print("  " + " ➔ ".join(ruta))
    else:
        print("No existe un Camino de Hamilton para esta red vial.")