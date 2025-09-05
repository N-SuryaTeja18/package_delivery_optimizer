from nodes_cluster import euclidean_distance


def build_cluster_graph(nodes, cluster_id):
    """Return adjacency matrix for a given cluster (warehouse + deliveries)."""
    cluster_nodes = [n for n in nodes if n.get("cluster") == cluster_id]
    n = len(cluster_nodes)
    dist_matrix = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                dist_matrix[i][j] = euclidean_distance(
                    (cluster_nodes[i]["x"], cluster_nodes[i]["y"]),
                    (cluster_nodes[j]["x"], cluster_nodes[j]["y"])
                )
    return cluster_nodes, dist_matrix


def nearest_neighbor_tsp(dist_matrix, start_index=0):
    """Simple nearest neighbor heuristic for TSP."""
    n = len(dist_matrix)
    unvisited = set(range(n))
    tour = [start_index]
    unvisited.remove(start_index)

    while unvisited:
        last = tour[-1]
        next_city = min(unvisited, key=lambda j: dist_matrix[last][j])
        tour.append(next_city)
        unvisited.remove(next_city)

    tour.append(start_index)  # return to start
    return tour


def tour_length(tour, dist_matrix):
    return sum(dist_matrix[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))
