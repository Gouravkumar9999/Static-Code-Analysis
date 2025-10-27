from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Global inventory dictionary mapping item -> quantity
stock_data: Dict[str, int] = {}


def add_item(item: str, qty: int, logs: Optional[List[str]] = None) -> None:
    """
    Add qty of item to stock_data. Positive qty only.
    Logs appended to logs list if provided.
    """
    if logs is None:
        logs = []

    if not isinstance(item, str):
        logging.error("add_item: item must be a string (got %r)", type(item))
        raise TypeError("item must be a string")

    if not isinstance(qty, int):
        logging.error("add_item: qty must be an integer (got %r)", type(qty))
        raise TypeError("qty must be an integer")

    if qty <= 0:
        logging.error("add_item: qty must be positive (got %d)", qty)
        raise ValueError("qty must be a positive integer")

    previous = stock_data.get(item, 0)
    stock_data[item] = previous + qty
    entry = f"{datetime.now().isoformat()}: Added {qty} of {item}"
    logs.append(entry)
    logging.info("Added %d of %s (previous: %d, now: %d)", qty, item, previous, stock_data[item])


def remove_item(item: str, qty: int) -> None:
    """
    Remove qty of item from stock_data. If quantity reduces to 0 or below,
    the item is removed from the dictionary.
    """
    if not isinstance(item, str):
        logging.error("remove_item: item must be a string (got %r)", type(item))
        raise TypeError("item must be a string")

    if not isinstance(qty, int):
        logging.error("remove_item: qty must be an integer (got %r)", type(qty))
        raise TypeError("qty must be an integer")

    if qty <= 0:
        logging.error("remove_item: qty must be positive (got %d)", qty)
        raise ValueError("qty must be a positive integer")

    current = stock_data.get(item)
    if current is None:
        logging.warning("remove_item: item %r not found in inventory", item)
        raise KeyError(f"Item '{item}' not found in inventory")

    if qty >= current:
        # Remove the item entirely
        del stock_data[item]
        logging.info("Removed item %r entirely (removed %d, had %d)", item, qty, current)
    else:
        stock_data[item] = current - qty
        logging.info("Removed %d of %s (remaining: %d)", qty, item, stock_data[item])


def get_qty(item: str) -> int:
    """
    Return quantity of item in stock (0 if missing).
    """
    if not isinstance(item, str):
        logging.error("get_qty: item must be a string (got %r)", type(item))
        raise TypeError("item must be a string")

    return stock_data.get(item, 0)


def load_data(file: str = "inventory.json") -> None:
    """
    Load inventory from a JSON file. If file doesn't exist or is invalid,
    initialize an empty inventory and log an error.
    """
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                logging.error("load_data: expected JSON object (dict), got %r", type(data))
                raise ValueError("inventory file does not contain a JSON object")
            # Convert quantities to ints where possible
            stock_data = {str(k): int(v) for k, v in data.items()}
            logging.info("Loaded inventory from %s", file)
    except FileNotFoundError:
        logging.warning("load_data: file %s not found. Starting with empty inventory.", file)
        stock_data = {}
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logging.error("load_data: failed to load %s (%s). Starting with empty inventory.", file, exc)
        stock_data = {}


def save_data(file: str = "inventory.json") -> None:
    """
    Save current inventory to a JSON file in a readable format.
    """
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=2, sort_keys=True)
        logging.info("Saved inventory to %s", file)
    except OSError as exc:
        logging.error("save_data: failed to write to %s (%s)", file, exc)
        raise


def print_data() -> None:
    """Print a simple inventory report to stdout."""
    logging.info("Inventory Report:")
    if not stock_data:
        logging.info("  (no items in inventory)")
        return

    for item, qty in sorted(stock_data.items()):
        logging.info("  %s -> %d", item, qty)


def check_low_items(threshold: int = 5) -> List[str]:
    """
    Return a list of item names whose quantity is below threshold.
    """
    if not isinstance(threshold, int):
        logging.error("check_low_items: threshold must be an integer (got %r)", type(threshold))
        raise TypeError("threshold must be an integer")

    if threshold < 0:
        logging.error("check_low_items: threshold must be non-negative (got %d)", threshold)
        raise ValueError("threshold must be non-negative")

    return [item for item, qty in stock_data.items() if qty < threshold]


def main() -> None:
    """Example usage of the inventory functions."""
    # Initialize or load prior state
    load_data()

    # Demonstrate adding and removing with proper validation
    try:
        add_item("apple", 10)
        # Intentionally demonstrate catching invalid inputs (wrapped in try/except for example)
        try:
            add_item("banana", -2)  # will raise ValueError
        except ValueError:
            logging.info("Skipped adding banana with invalid quantity")

        # Demonstrate type validation
        try:
            add_item(123, 10)  # type error: item must be string
        except TypeError:
            logging.info("Skipped adding item with invalid name type")

        remove_item("apple", 3)
        try:
            remove_item("orange", 1)
        except KeyError:
            logging.info("Tried to remove non-existent item 'orange'")

        logging.info("Apple stock: %d", get_qty("apple"))
        logging.info("Low items: %s", check_low_items())
    finally:
        # Save and print current inventory
        save_data()
        print_data()

    # Replacing the dangerous eval usage with a safe log statement:
    logging.debug("Demo: eval() removed for safety; no dynamic code execution performed.")


if __name__ == "__main__":
    main()
