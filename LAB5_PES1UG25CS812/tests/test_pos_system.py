"""Regression tests for the Retail POS application."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pos_system


class RetailPosTests(unittest.TestCase):
    """Test checkout, promotions, stock updates, and receipt logging."""

    def setUp(self) -> None:
        pos_system.SALES_STATE["total"] = 0.0
        pos_system.RECEIPT_LINES.clear()
        pos_system.STOCK.update(
            {"pen": 100, "notebook": 50, "bag": 20, "bottle": 40}
        )

    def test_checkout_calculates_tax_and_records_receipt(self) -> None:
        receipts: list[float] = []
        total = pos_system.process_checkout(
            [("pen", 2), ("notebook", 1)],
            receipts=receipts,
        )
        self.assertEqual(total, 68.25)
        self.assertEqual(receipts, [68.25])
        self.assertEqual(pos_system.SALES_STATE["total"], 68.25)

    def test_checkout_rejects_unknown_product(self) -> None:
        with self.assertRaises(ValueError):
            pos_system.process_checkout([("laptop", 1)])

    def test_checkout_rejects_non_positive_quantity(self) -> None:
        with self.assertRaises(ValueError):
            pos_system.process_checkout([("pen", 0)])

    def test_checkout_rejects_invalid_tax_rate(self) -> None:
        with self.assertRaises(ValueError):
            pos_system.process_checkout([("pen", 1)], tax_rate=-0.1)

    def test_checkout_rejects_string_quantity(self) -> None:
        with self.assertRaises(TypeError):
            pos_system.process_checkout(
                [("pen", "2")]
            )  # type: ignore[list-item]

    def test_promo_codes_apply_only_allowed_discounts(self) -> None:
        self.assertEqual(pos_system.apply_promo_code("SAVE10", 100), 90.0)
        self.assertEqual(pos_system.apply_promo_code("SAVE50", 30), 0.0)
        self.assertEqual(pos_system.apply_promo_code("CLEAR", 100), 100.0)

    def test_unknown_promo_code_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            pos_system.apply_promo_code("total * 0.9", 100)

    def test_stock_update_changes_inventory(self) -> None:
        self.assertEqual(pos_system.update_stock("pen", 5), 105)

    def test_receipt_log_is_written(self) -> None:
        pos_system.process_checkout([("pen", 1)])
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = Path(temp_dir) / "pos_log.txt"
            pos_system.save_receipt_log(log_path)
            self.assertIn("Receipt #1", log_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
