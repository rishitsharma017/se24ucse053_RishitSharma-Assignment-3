import heapq
import matplotlib.pyplot as plt
import networkx as nx

# Indian cities and road distances (in km) - real approximate distances
graph = {
    'Delhi': {'Jaipur': 281, 'Agra': 233, 'Chandigarh': 274, 'Lucknow': 555, 'Amritsar': 449},
    'Jaipur': {'Delhi': 281, 'Agra': 240, 'Ahmedabad': 670, 'Jodhpur': 343, 'Mumbai': 1158},
    'Agra': {'Delhi': 233, 'Jaipur': 240, 'Lucknow': 363, 'Gwalior': 119, 'Kanpur': 293},
    'Chandigarh': {'Delhi': 274, 'Amritsar': 229, 'Shimla': 117},
    'Amritsar': {'Delhi': 449, 'Chandigarh': 229},
    'Shimla': {'Chandigarh': 117},
    'Lucknow': {'Delhi': 555, 'Agra': 363, 'Kanpur': 84, 'Varanasi': 286, 'Allahabad': 200},
    'Kanpur': {'Lucknow': 84, 'Agra': 293, 'Allahabad': 192},
    'Allahabad': {'Lucknow': 200, 'Kanpur': 192, 'Varanasi': 125, 'Patna': 467},
    'Varanasi': {'Lucknow': 286, 'Allahabad': 125, 'Patna': 300},
    'Patna': {'Varanasi': 300, 'Allahabad': 467, 'Kolkata': 600},
    'Gwalior': {'Agra': 119, 'Bhopal': 423},
    'Bhopal': {'Gwalior': 423, 'Nagpur': 357, 'Indore': 195, 'Ahmedabad': 656},
    'Indore': {'Bhopal': 195, 'Ahmedabad': 400, 'Mumbai': 591},
    'Ahmedabad': {'Jaipur': 670, 'Bhopal': 656, 'Indore': 400, 'Mumbai': 524, 'Surat': 265},
    'Surat': {'Ahmedabad': 265, 'Mumbai': 284},
    'Mumbai': {'Ahmedabad': 524, 'Surat': 284, 'Pune': 149, 'Goa': 597, 'Hyderabad': 711, 'Indore': 591, 'Jaipur': 1158},
    'Pune': {'Mumbai': 149, 'Hyderabad': 560, 'Goa': 450},
    'Goa': {'Mumbai': 597, 'Pune': 450, 'Bangalore': 560},
    'Nagpur': {'Bhopal': 357, 'Hyderabad': 503, 'Kolkata': 1054},
    'Hyderabad': {'Mumbai': 711, 'Pune': 560, 'Nagpur': 503, 'Bangalore': 575, 'Chennai': 627},
    'Bangalore': {'Hyderabad': 575, 'Goa': 560, 'Chennai': 346, 'Mysore': 143, 'Kochi': 545},
    'Chennai': {'Hyderabad': 627, 'Bangalore': 346, 'Madurai': 462},
    'Mysore': {'Bangalore': 143, 'Kochi': 463},
    'Kochi': {'Bangalore': 545, 'Mysore': 463, 'Madurai': 210},
    'Madurai': {'Chennai': 462, 'Kochi': 210},
    'Kolkata': {'Patna': 600, 'Nagpur': 1054, 'Bhubaneswar': 440},
    'Bhubaneswar': {'Kolkata': 440, 'Hyderabad': 720},
}


def dijkstra(graph, start, end):
    """
    Dijkstra's Algorithm - finds shortest path between two cities.
    Returns (distance, path)
    """
    # Priority queue: (cost, current_node, path)
    pq = [(0, start, [start])]
    visited = set()

    while pq:
        cost, node, path = heapq.heappop(pq)

        if node in visited:
            continue
        visited.add(node)

        if node == end:
            return cost, path

        for neighbor, weight in graph.get(node, {}).items():
            if neighbor not in visited:
                heapq.heappush(pq, (cost + weight, neighbor, path + [neighbor]))

    return float('inf'), []


def find_all_shortest_paths(graph, start):
    """Find shortest distances from start to all other cities."""
    distances = {city: float('inf') for city in graph}
    distances[start] = 0
    previous = {city: None for city in graph}
    pq = [(0, start)]

    while pq:
        cost, node = heapq.heappop(pq)
        for neighbor, weight in graph.get(node, {}).items():
            new_cost = cost + weight
            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                previous[neighbor] = node
                heapq.heappush(pq, (new_cost, neighbor))

    return distances, previous


def reconstruct_path(previous, start, end):
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()
    return path if path[0] == start else []


def visualize_graph(graph, path=None, title="Indian Cities Road Network"):
    G = nx.Graph()
    for city, neighbors in graph.items():
        for neighbor, dist in neighbors.items():
            G.add_edge(city, neighbor, weight=dist)

    pos = nx.spring_layout(G, seed=42, k=2)
    plt.figure(figsize=(16, 12))

    # Draw all edges
    nx.draw_networkx_edges(G, pos, alpha=0.3, edge_color='gray')

    # Highlight shortest path edges
    if path and len(path) > 1:
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                               edge_color='red', width=3, alpha=0.8)

    nx.draw_networkx_nodes(G, pos, node_color='lightblue',
                           node_size=800, alpha=0.9)

    # Highlight path nodes
    if path:
        nx.draw_networkx_nodes(G, pos, nodelist=path,
                               node_color='orange', node_size=1000)
        nx.draw_networkx_nodes(G, pos, nodelist=[path[0], path[-1]],
                               node_color='red', node_size=1200)

    nx.draw_networkx_labels(G, pos, font_size=7, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=5)

    plt.title(title, fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('india_road_network.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Graph saved as 'india_road_network.png'")


# ─── MAIN ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("       DIJKSTRA'S ALGORITHM - INDIAN CITIES")
    print("=" * 60)

    # Example: Delhi to Chennai
    start_city = "Delhi"
    end_city = "Chennai"

    distance, path = dijkstra(graph, start_city, end_city)
    print(f"\nShortest path from {start_city} to {end_city}:")
    print(f"  Path     : {' → '.join(path)}")
    print(f"  Distance : {distance} km")

    # Show all distances from Delhi
    print(f"\nAll shortest distances from {start_city}:")
    print("-" * 40)
    distances, previous = find_all_shortest_paths(graph, start_city)
    for city, dist in sorted(distances.items(), key=lambda x: x[1]):
        if dist != float('inf') and city != start_city:
            p = reconstruct_path(previous, start_city, city)
            print(f"  {city:<15} : {dist:>5} km  |  {' → '.join(p)}")

    # Visualize
    print("\nGenerating graph visualization...")
    visualize_graph(graph, path,
                    title=f"Shortest Path: {start_city} → {end_city} ({distance} km)")
