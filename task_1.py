from collections import deque
import networkx as nx
import matplotlib.pyplot as plt


def create_logistics_graph():
    G = nx.DiGraph()
    edges = [
        ("Термінал 1", "Склад 1", 25),
        ("Термінал 1", "Склад 2", 20),
        ("Термінал 1", "Склад 3", 15),
        ("Термінал 2", "Склад 3", 15),
        ("Термінал 2", "Склад 4", 30),
        ("Термінал 2", "Склад 2", 10),
        ("Склад 1", "Магазин 1", 15),
        ("Склад 1", "Магазин 2", 10),
        ("Склад 1", "Магазин 3", 20),
        ("Склад 2", "Магазин 4", 15),
        ("Склад 2", "Магазин 5", 10),
        ("Склад 2", "Магазин 6", 25),
        ("Склад 3", "Магазин 7", 20),
        ("Склад 3", "Магазин 8", 15),
        ("Склад 3", "Магазин 9", 10),
        ("Склад 4", "Магазин 10", 20),
        ("Склад 4", "Магазин 11", 10),
        ("Склад 4", "Магазин 12", 15),
        ("Склад 4", "Магазин 13", 5),
        ("Склад 4", "Магазин 14", 10),
    ]
    G.add_weighted_edges_from(edges)
    return G


def add_super_source_sink(
    G, terminals, stores, super_source="Джерело", super_sink="Сток"
):
    """
    Adds a super source node and a super sink node to the given graph.

    The super source node is connected to all terminals with infinite capacity edges,
    while the super sink node is connected to all stores with infinite capacity edges.

    Args:
        G (nx.DiGraph): The graph to add the super source and super sink nodes to.
        terminals (List[str]): The list of terminal nodes to connect to the super source node.
        stores (List[str]): The list of store nodes to connect to the super sink node.
        super_source (str): The name of the super source node.
        super_sink (str): The name of the super sink node.
    """
    for terminal in terminals:
        G.add_edge(super_source, terminal, weight=float("inf"))
    for store in stores:
        G.add_edge(store, super_sink, weight=float("inf"))


def build_capacity_matrix(G, node_indices):
    """
    Builds a capacity matrix from the given graph and node indices.

    Args:
        G (nx.DiGraph): The graph to build the capacity matrix from.
        node_indices (Dict[str, int]): A dictionary mapping node names to their indices in the matrix.

    Returns:
        List[List[int]]: A 2D list representing the capacity matrix, where matrix[i][j] is the capacity of the edge from node i to node j.

    Raises:
        ValueError: If the graph contains edges with negative or zero capacity.
    """
    n = len(node_indices)
    matrix = [[0] * n for _ in range(n)]
    for u, v, data in G.edges(data=True):
        i, j = node_indices[u], node_indices[v]
        matrix[i][j] = data["weight"]
    return matrix


def bfs(capacity, flow, source, sink, parent):
    visited = [False] * len(capacity)
    queue = deque([source])
    visited[source] = True

    while queue:
        u = queue.popleft()
        for v in range(len(capacity)):
            if not visited[v] and capacity[u][v] - flow[u][v] > 0:
                parent[v] = u
                visited[v] = True
                if v == sink:
                    return True
                queue.append(v)
    return False


def edmonds_karp(capacity, source, sink):
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]
    parent = [-1] * n
    max_flow = 0

    while bfs(capacity, flow, source, sink, parent):
        path_flow = float("inf")
        s = sink
        while s != source:
            path_flow = min(path_flow, capacity[parent[s]][s] - flow[parent[s]][s])
            s = parent[s]
        v = sink
        while v != source:
            u = parent[v]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = parent[v]
        max_flow += path_flow

    return max_flow, flow


def print_flow_table(flow, node_indices, terminals, warehouses, store_range):
    print("Таблиця фактичних потоків (термінал - магазин):")
    for term in terminals:
        term_idx = node_indices[term]
        for store_num in store_range:
            store = f"Магазин {store_num}"
            store_idx = node_indices[store]
            total_flow = 0
            for warehouse in warehouses:
                warehouse_idx = node_indices[warehouse]
                if (
                    flow[warehouse_idx][store_idx] > 0
                    and flow[term_idx][warehouse_idx] > 0
                ):
                    total_flow += min(
                        flow[warehouse_idx][store_idx], flow[term_idx][warehouse_idx]
                    )
            if total_flow > 0:
                print(f"{term} - {store}: {total_flow} од.")


def draw_graph(G, pos):
    plt.figure(figsize=(15, 10))
    visible_nodes = [node for node in G.nodes if node in pos]
    visible_edges = [(u, v) for u, v in G.edges if u in pos and v in pos]
    visible_labels = {(u, v): G[u][v]["weight"] for u, v in visible_edges}

    nx.draw(
        G.subgraph(visible_nodes),
        pos,
        with_labels=True,
        node_size=2000,
        node_color="skyblue",
        font_size=12,
        arrows=True,
    )
    nx.draw_networkx_edge_labels(G, pos, edge_labels=visible_labels)
    plt.title("Логістична мережа (граф потоків)")
    plt.show()



G = create_logistics_graph()

positions = {
    "Термінал 1": (-1, 0),
    "Термінал 2": (3, 0),
    "Склад 1": (0, 1.5),
    "Склад 2": (2, 1.5),
    "Склад 3": (0, -1.5),
    "Склад 4": (2, -1.5),
    "Магазин 1": (-2, 3),
    "Магазин 2": (-1, 3),
    "Магазин 3": (0, 3),
    "Магазин 4": (1, 3),
    "Магазин 5": (2, 3),
    "Магазин 6": (3, 3),
    "Магазин 7": (-2, -3),
    "Магазин 8": (-1, -3),
    "Магазин 9": (0, -3),
    "Магазин 10": (1, -3),
    "Магазин 11": (2, -3),
    "Магазин 12": (3, -3),
    "Магазин 13": (4, -3),
    "Магазин 14": (5, -3),
}

super_source = "Джерело"
super_sink = "Сток"

terminals = ["Термінал 1", "Термінал 2"]
warehouses = ["Склад 1", "Склад 2", "Склад 3", "Склад 4"]
stores = [f"Магазин {i}" for i in range(1, 15)]

add_super_source_sink(G, terminals, stores, super_source, super_sink)

nodes = list(G.nodes)
node_indices = {node: i for i, node in enumerate(nodes)}
capacity_matrix = build_capacity_matrix(G, node_indices)

source_idx = node_indices[super_source]
sink_idx = node_indices[super_sink]

max_flow, flow = edmonds_karp(capacity_matrix, source_idx, sink_idx)

print(f"Максимальний потік у логістичній мережі: {max_flow}")
print_flow_table(flow, node_indices, terminals, warehouses, range(1, 15))

draw_graph(G, positions)
