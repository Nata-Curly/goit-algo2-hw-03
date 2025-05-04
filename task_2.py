import csv
from timeit import timeit
from typing import Dict, List, Tuple
from BTrees.OOBTree import OOBTree


CSV_FILE = "./generated_items_data.csv"


def load_items_from_csv(file_path: str) -> List[Tuple[int, Dict]]:
    """
    Loads items from a CSV file and returns them as a list of tuples.

    Each tuple contains an integer item ID and a dictionary with item details
    such as name, category, and price.

    Args:
        file_path (str): The path to the CSV file containing item data.

    Returns:
        List[Tuple[int, Dict]]: A list of tuples where each tuple consists of
        an item ID and a dictionary with the item's details.
    """

    items = []
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item_id = int(row["ID"])
            item = {
                "Name": row["Name"],
                "Category": row["Category"],
                "Price": float(row["Price"]),
            }
            items.append((item_id, item))
    return items


def add_item_to_tree(tree: OOBTree, item_id: int, item: Dict):
    """
    Adds an item to the given OOBTree.

    Args:
        tree (OOBTree): The OOBTree to add the item to.
        item_id (int): The ID of the item to add.
        item (Dict): The item to add, represented as a dictionary with keys
            "Name", "Category", and "Price".
    """
    tree[item_id] = item


def add_item_to_dict(store: Dict[int, Dict], item_id: int, item: Dict):
    """
    Adds an item to the given dictionary-based store.

    Args:
        store (Dict[int, Dict]): The dictionary-based store to add the item to.
        item_id (int): The ID of the item to add.
        item (Dict): The item to add, represented as a dictionary with keys
            "Name", "Category", and "Price".
    """

    store[item_id] = item


def range_query_tree(tree: OOBTree, min_price: float, max_price: float) -> List[Dict]:
    """
    Retrieves a list of items from the OOBTree whose prices fall within the specified range.

    Args:
        tree (OOBTree): The OOBTree containing items to query.
        min_price (float): The minimum price of the range.
        max_price (float): The maximum price of the range.

    Returns:
        List[Dict]: A list of dictionaries representing the items with prices within the specified range.
    """

    return [item for _, item in tree.items() if min_price <= item["Price"] <= max_price]


def range_query_dict(
    store: Dict[int, Dict], min_price: float, max_price: float
) -> List[Dict]:
    """
    Retrieves a list of items from the dictionary-based store whose prices fall within the specified range.

    Args:
        store (Dict[int, Dict]): The dictionary-based store containing items to query.
        min_price (float): The minimum price of the range.
        max_price (float): The maximum price of the range.

    Returns:
        List[Dict]: A list of dictionaries representing the items with prices within the specified range.
    """

    return [item for item in store.values() if min_price <= item["Price"] <= max_price]


def main():
    items = load_items_from_csv(CSV_FILE)

    tree = OOBTree()
    store = {}

    for item_id, item in items:
        add_item_to_tree(tree, item_id, item)
        add_item_to_dict(store, item_id, item)

    price_min = 50.0
    price_max = 150.0

    time_tree = timeit(
        stmt=lambda: range_query_tree(tree, price_min, price_max), number=100
    )

    time_dict = timeit(
        stmt=lambda: range_query_dict(store, price_min, price_max), number=100
    )

    print(f"Total range_query time for OOBTree: {time_tree:.6f} seconds")
    print(f"Total range_query time for Dict: {time_dict:.6f} seconds")


if __name__ == "__main__":
    main()
