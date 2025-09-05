import random
import math
from sklearn.cluster import KMeans

SEED = 100
random.seed(SEED)


def euclidean_distance(a, b):
    return round(math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2), 2)


def generate_nodes(num_nodes, num_warehouses):
    nodes = []
    for i in range(num_nodes):
        nodes.append({
            "id": i,
            "x": round(random.uniform(0, 100), 2),
            "y": round(random.uniform(0, 100), 2),
            "type": "D"  # Default as delivery
        })

    # Randomly choose warehouse IDs
    warehouse_ids = random.sample(range(num_nodes), num_warehouses)
    for wid in warehouse_ids:
        nodes[wid]["type"] = "W"

    return nodes


def cluster_nodes(nodes, num_clusters):
    delivery_nodes = [node for node in nodes if node["type"] == "D"]
    delivery_coords = [(node["x"], node["y"]) for node in delivery_nodes]

    # Run KMeans
    kmeans = KMeans(n_clusters=num_clusters, random_state=SEED, n_init=10)
    labels = kmeans.fit_predict(delivery_coords)

    # Assign cluster to deliveries
    for node, label in zip(delivery_nodes, labels):
        node["cluster"] = int(label)

    # Assign warehouses to nearest cluster center
    warehouse_nodes = [node for node in nodes if node["type"] == "W"]
    available_warehouses = warehouse_nodes[:]

    for cluster_id, centroid in enumerate(kmeans.cluster_centers_):
        nearest_warehouse = min(
            available_warehouses,
            key=lambda w: euclidean_distance((w["x"], w["y"]), centroid)
        )
        nearest_warehouse["cluster"] = cluster_id
        available_warehouses.remove(nearest_warehouse)
    return nodes, kmeans.cluster_centers_, labels, warehouse_nodes