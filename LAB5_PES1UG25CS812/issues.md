# Lab 5 — Static Code Analysis Issues

**Student:** Dhanush Gowda A S  
**SRN:** PES1UG25CS812  
**Program:** Retail Point of Sale & Discount Tracker

The line references below refer to the supplied starter file. Severity is based on likely impact.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Dynamic execution of promo input with `eval()` | Security — High | 24–26 | User-controlled text is executed as Python code, allowing arbitrary code execution. | Replace expressions with a fixed allow-list of promo codes and explicit arithmetic. |
| Broad bare exception hides invalid cart entries | Reliability — High | 14–18 | Every error is silently converted to a zero contribution, concealing unknown products and invalid quantities. | Validate product names and quantities and raise specific exceptions. |
| Mutable default argument `receipts=[]` | Correctness — Medium | 11 | The same list is reused across calls, so receipt totals leak between checkouts. | Use `None` as the default and append only to a caller-provided list. |
| Negative quantities and tax rates accepted | Correctness — Medium | 13–21 | Negative quantities or invalid tax rates can produce negative or misleading bills. | Require positive integer quantities and tax rates in the range 0–1. |
| Receipt file handle is not closed deterministically | Resource management — Medium | 37–40 | The open file is not protected by a context manager; buffered output may not be flushed promptly. | Use `with open(...)` (implemented with `Path.open`). |
| Stock update does not update stock | Functional defect — Medium | 29–35 | The code reassigns the product's price to itself and ignores the requested quantity. | Maintain a stock dictionary and increment the stock count after validation. |
| Broad exception is swallowed in stock update | Reliability — Medium | 30–35 | Unknown products and other failures are hidden, so callers cannot tell the update failed. | Validate the product and raise a clear `ValueError`. |
| Non-PEP 8 function name and unused imports | Maintainability — Low | 2–3, 42–43 | `printSales` is not snake_case; `json` and `logging` are unused in the starter. | Use `print_sales`; remove unused imports or use logging appropriately. |

## Fixes implemented

1. Removed `eval()`; only `SAVE10`, `SAVE50`, and `CLEAR` are accepted.
2. Removed silent broad exception handling and added explicit product/quantity validation.
3. Removed the mutable list default and made receipt collection optional.
4. Validated positive quantities and a tax-rate range of 0 through 1.
5. Used a context manager and UTF-8 encoding for receipt logging.
6. Added a real stock dictionary and update operation.
7. Renamed `printSales()` to `print_sales()` and added module/function docstrings.
8. Protected the demonstration with the `if __name__ == "__main__"` guard.

## Static-analysis commands

Run these from this directory after installing the tools:

```bash
python -m pip install pylint bandit flake8
python pos_system.py
pylint pos_system.py
bandit -q -r pos_system.py
flake8 pos_system.py
```

Save reproducible reports with:

```bash
pylint pos_system.py > pylint_report.txt
bandit -r pos_system.py > bandit_report.txt
flake8 pos_system.py > flake8_report.txt
```

**Verification note:** The final source has been reviewed for the documented defects. Tool scores and report contents are environment-dependent and are intentionally not fabricated here. Run the commands above in the course environment and retain the actual outputs for submission.
