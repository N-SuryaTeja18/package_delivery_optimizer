import matplotlib.pyplot as plt
from new import generate_nodes, cluster_nodes

nodes = generate_nodes()
cluster_nodes(nodes)

def plot_clusters(nodes, labels, warehouses, num_clusters):
    """
    nodes: dict {node_id: (x, y)}
    labels: list of cluster IDs for each node (same order as nodes.keys())
    warehouses: list of warehouse IDs
    num_clusters: number of clusters
    """

    # Generate colors for clusters
    colors = plt.cm.get_cmap("tab10", num_clusters)

    # Scatter plot for delivery points
    for node_id, (x, y) in nodes.items():
        cluster_id = labels[node_id]
        if node_id in warehouses:
            plt.scatter(x, y, c=[colors(cluster_id)], marker="s", s=150, edgecolors="black", label=f"Warehouse {node_id}" if f"W{node_id}" not in plt.gca().get_legend_handles_labels()[1] else "")
        else:
            plt.scatter(x, y, c=[colors(cluster_id)], label=f"Cluster {cluster_id}" if f"Cluster {cluster_id}" not in plt.gca().get_legend_handles_labels()[1] else "")

    # Labels & title
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("Package Delivery Clustering")
    plt.legend()
    plt.grid(True)
    plt.show()
