import csv
import os
import re

DELIVERY_FILE = "deliveries.csv"

# Define node types: W = Warehouse, D = Delivery, N = Normal
node_types = {i: 'N' for i in range(30)}
for wh in [0, 8, 28]:
    node_types[wh] = 'W'

# Hardcoded graph edges with weights
graph = {
    0:  [(1, 4), (5, 6)],
    1:  [(0, 4), (2, 3), (6, 5)],
    2:  [(1, 3), (3, 2)],
    3:  [(2, 2), (4, 7)],
    4:  [(3, 7), (9, 3)],
    5:  [(0, 6), (10, 2)],
    6:  [(1, 5), (11, 4)],
    7:  [(8, 6), (12, 3)],
    8:  [(7, 6), (9, 5)],
    9:  [(4, 3), (8, 5), (14, 2)],
    10: [(5, 2), (11, 3), (15, 6)],
    11: [(6, 4), (10, 3), (12, 5)],
    12: [(7, 3), (11, 5), (13, 3)],
    13: [(12, 3), (14, 4)],
    14: [(9, 2), (13, 4), (19, 5)],
    15: [(10, 6), (16, 2)],
    16: [(15, 2), (17, 3)],
    17: [(16, 3), (18, 6)],
    18: [(17, 6), (19, 4)],
    19: [(14, 5), (18, 4), (24, 3)],
    20: [(21, 3), (25, 6)],
    21: [(20, 3), (22, 2), (26, 5)],
    22: [(21, 2), (23, 3)],
    23: [(22, 3), (24, 5)],
    24: [(19, 3), (23, 5), (29, 4)],
    25: [(20, 6), (26, 3), (27, 4)],
    26: [(25, 3), (21, 5), (28, 2)],
    27: [(25, 4), (28, 3)],
    28: [(27, 3), (29, 5), (26, 2)],
    29: [(24, 4), (28, 5)]
}

# Create delivery file if it doesn't exist
if not os.path.exists(DELIVERY_FILE):
    with open(DELIVERY_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["package_id", "delivery_point", "time_window_start", "time_window_end"])
else:
    with open(DELIVERY_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                dp = int(row["delivery_point"])
                if dp not in [0, 8, 28]:
                    node_types[dp] = 'D'
            except:
                continue


def is_valid_time(t):
    return re.match(r'^([01]\d|2[0-3]):[0-5]\d$', t)


def package_exists(package_id):
    with open(DELIVERY_FILE, "r") as f:
        reader = csv.DictReader(f)
        return any(row["package_id"] == package_id for row in reader)


def add_delivery():
    package_id = input("Enter Package ID: ").strip()
    if package_exists(package_id):
        print("Package ID already exists.")
        return

    try:
        point = int(input("Enter Delivery Point (0–29): "))
        if point < 0 or point > 29:
            raise ValueError
        if node_types[point] == 'W':
            print("This node is a warehouse. Cannot deliver here.")
            return
    except ValueError:
        print("Invalid delivery point.")
        return

    time_start = input("Enter Time Window Start (HH:MM): ").strip()
    time_end = input("Enter Time Window End (HH:MM): ").strip()

    if not (is_valid_time(time_start) and is_valid_time(time_end)):
        print("Time must be in HH:MM 24-hr format.")
        return

    # Append to CSV
    with open(DELIVERY_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([package_id, point, time_start, time_end])

    node_types[point] = 'D'
    print("Delivery added.")


def remove_delivery():
    package_id = input("Enter Package ID to Remove: ").strip()
    updated = []
    found = False
    removed_point = None

    with open(DELIVERY_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["package_id"] != package_id:
                updated.append(row)
            else:
                found = True
                removed_point = int(row["delivery_point"])

    if not found:
        print("Package ID not found.")
        return

    # Update file
    with open(DELIVERY_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["package_id", "delivery_point", "time_window_start", "time_window_end"])
        writer.writeheader()
        writer.writerows(updated)

    # Update node type
    if removed_point not in [0, 8, 28]:
        node_types[removed_point] = 'N'

    print("Delivery removed.")


def list_deliveries():
    print("\n--- Current Deliveries ---")
    with open(DELIVERY_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f'Package ID: {row["package_id"]}, Point: {row["delivery_point"]}, '
                  f'Time: {row["time_window_start"]}–{row["time_window_end"]}')
    print("--------------------------\n")


# CLI loop
if __name__ == "__main__":
    while True:
        print(
            """
            --- Delivery CLI ---
            1. Add Delivery Point
            2. Remove Delivery Point
            3. List Deliveries
            4. Exit
            """
        )
        print(node_types[0])
        choice = input("Choose an option: ").strip()
        if choice == '1':
            add_delivery()
        elif choice == '2':
            remove_delivery()
        elif choice == '3':
            list_deliveries()
        elif choice == '4':
            break
        else:
            print("Invalid option.")