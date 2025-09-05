from nodes_cluster import generate_nodes, cluster_nodes
from graph_tsp import build_cluster_graph, nearest_neighbor_tsp, tour_length

NUM_NODES = 30
NUM_WAREHOUSES = 3
NUM_CLUSTERS = 3


def main():
    nodes = generate_nodes(NUM_NODES, NUM_WAREHOUSES)
    nodes, centers, labels, warehouse_nodes = cluster_nodes(nodes, NUM_CLUSTERS)

    # Solve TSP for each cluster
    for cluster_id in range(NUM_CLUSTERS):
        cluster_nodes_list, dist_matrix = build_cluster_graph(nodes, cluster_id)

        # Find warehouse index in this cluster
        warehouse_index = next(
            i for i, n in enumerate(cluster_nodes_list) if n["type"] == "W"
        )

        # Run nearest neighbor TSP
        route = nearest_neighbor_tsp(dist_matrix, start_index=warehouse_index)
        length = tour_length(route, dist_matrix)

        # Convert indices -> node IDs
        route_nodes = [cluster_nodes_list[i]["id"] for i in route]

        print(f"\nCluster {cluster_id}:")
        print("Route (warehouse + deliveries):", route_nodes)
        print("Total distance:", length)


if __name__ == "__main__":
    main()
