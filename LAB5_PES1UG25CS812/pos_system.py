"""Retail point-of-sale and discount tracker.

The module exposes small, testable functions for checkout, promo application,
stock tracking, and receipt logging. Run it directly for a demonstration.
"""

from __future__ import annotations

import logging
import random
from pathlib import Path
from typing import Iterable, Mapping, Sequence

PRICE_LIST: dict[str, float] = {
    "pen": 10.0,
    "notebook": 45.0,
    "bag": 799.0,
    "bottle": 150.0,
}
TAX_RATE = 0.05
SALES_TOTAL = 0.0
RECEIPT_LINES: list[str] = []
STOCK: dict[str, int] = {
    "pen": 100,
    "notebook": 50,
    "bag": 20,
    "bottle": 40,
}

LOGGER = logging.getLogger(__name__)


def process_checkout(
    cart_items: Iterable[tuple[str, int]],
    tax_rate: float = TAX_RATE,
    receipts: list[float] | None = None,
) -> float:
    """Calculate a bill, update sales, and append the total to receipts."""
    global SALES_TOTAL

    if not 0 <= tax_rate <= 1:
        raise ValueError("tax_rate must be between 0 and 1")

    subtotal = 0.0
    for item_name, quantity in cart_items:
        if item_name not in PRICE_LIST:
            raise ValueError(f"Unknown product: {item_name}")
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise TypeError("quantity must be an integer")
        if quantity <= 0:
            raise ValueError("quantity must be greater than zero")
        subtotal += PRICE_LIST[item_name] * quantity

    total = round(subtotal * (1 + tax_rate), 2)
    SALES_TOTAL = round(SALES_TOTAL + total, 2)

    if receipts is not None:
        receipts.append(total)

    receipt_number = random.randint(1000, 9999)
    RECEIPT_LINES.append(f"Receipt #{receipt_number} total={total:.2f}")
    return total


def apply_promo_code(code_str: str, total: float | None = None) -> float:
    """Apply an allow-listed promo code without evaluating user expressions."""
    amount = SALES_TOTAL if total is None else total
    normalized_code = code_str.strip().upper()

    if normalized_code == "SAVE10":
        discounted = amount * 0.90
    elif normalized_code == "SAVE50":
        discounted = max(0.0, amount - 50.0)
    elif normalized_code == "CLEAR":
        discounted = amount
    else:
        raise ValueError("Invalid promo code. Use SAVE10, SAVE50, or CLEAR.")

    return round(discounted, 2)


def update_stock(item: str, qty: int) -> int:
    """Increase an existing product's stock and return its new quantity."""
    if item not in STOCK:
        raise ValueError(f"Unknown product: {item}")
    if not isinstance(qty, int) or isinstance(qty, bool):
        raise TypeError("stock quantity must be an integer")
    if qty <= 0:
        raise ValueError("stock quantity must be greater than zero")

    STOCK[item] += qty
    LOGGER.info("Stock updated for %s by %d; available=%d", item, qty, STOCK[item])
    return STOCK[item]


def save_receipt_log(file: str | Path = "pos_log.txt") -> None:
    """Append current receipt lines to a log using a managed file handle."""
    log_path = Path(file)
    with log_path.open("a", encoding="utf-8") as receipt_file:
        for line in RECEIPT_LINES:
            receipt_file.write(f"{line}\n")


def print_sales() -> None:
    """Display the current sales total."""
    print(f"Sales so far: {SALES_TOTAL:.2f}")


def main() -> None:
    """Run representative checkout and promo examples."""
    demo_receipts: list[float] = []
    print("Bill 1:", process_checkout([("pen", 3), ("notebook", 2)], receipts=demo_receipts))
    print("Bill 2:", process_checkout([("bag", 1)], receipts=demo_receipts))
    print("After SAVE10:", apply_promo_code("SAVE10"))
    print("After SAVE50:", apply_promo_code("SAVE50"))
    update_stock("pen", 5)
    save_receipt_log()
    print_sales()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    main()
