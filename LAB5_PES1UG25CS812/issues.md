# Lab 5 — Static Code Analysis Issues

**Student:** Dhanush Gowda A S  
**SRN:** PES1UG25CS812  
**Program:** Retail Point of Sale & Discount Tracker

The line references below refer to the supplied starter file. Severity is based on likely impact.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Dynamic execution of promo input with `eval()` | Security — High | 24–27 | User-controlled text is executed as Python code, allowing arbitrary code execution. | Replace expressions with a fixed allow-list of promo codes and explicit arithmetic. |
| Broad bare exception hides invalid cart entries | Reliability — High | 13–17 | Every error is silently converted to a zero contribution, concealing unknown products and invalid quantities. | Validate product names and quantities and raise specific exceptions. |
| Mutable default argument `receipts=[]` | Correctness — Medium | 10 | The same list is reused across calls, so receipt totals leak between checkouts. | Use `None` as the default and append only to a caller-provided list. |
| Negative quantities and tax rates accepted | Correctness — Medium | 13–18, 47–48 | Negative quantities or invalid tax rates can produce negative or misleading bills. | Require positive integer quantities and tax rates in the range 0–1. |
| Receipt file handle is not closed deterministically | Resource management — Medium | 36–39 | The open file is not protected by a context manager; buffered output may not be flushed promptly. | Use a context manager and UTF-8 encoding for receipt logging. |
| Stock update does not update stock | Functional defect — Medium | 29–32 | The code reassigns the product's price to itself and ignores the requested quantity. | Maintain a stock dictionary and increment the stock count after validation. |
| Broad exception is swallowed in stock update | Reliability — Medium | 30–34 | Unknown products and other failures are hidden, so callers cannot tell the update failed. | Validate the product and raise a clear `ValueError`. |
| Non-PEP 8 function name and unused imports | Maintainability — Low | 1, 3, 41 | `printSales` is not snake_case; `json` and `logging` are unused in the starter. | Use `print_sales`; remove unused imports or use logging appropriately. |

## Fixes implemented

1. Removed `eval()`; only `SAVE10`, `SAVE50`, and `CLEAR` are accepted.
2. Removed silent broad exception handling and added explicit product/quantity validation.
3. Removed the mutable list default and made receipt collection optional.
4. Validated positive quantities and a numeric tax rate in the range 0 through 1.
5. Used a context manager and UTF-8 encoding for receipt logging.
6. Added a real stock dictionary and update operation.
7. Renamed `printSales()` to `print_sales()` and added module/function docstrings.
8. Replaced the global scalar sales total with a state dictionary to avoid reassignment of global state.
9. Added regression tests for billing, input validation, promos, inventory, and logging.

## Static-analysis commands

Run these from this directory after installing the tools:

```bash
python -m pip install -r requirements.txt
python pos_system.py
python -m unittest discover -s tests -v
python run_analysis.py
```

The helper creates `pylint_report.txt`, `bandit_report.txt`, and `flake8_report.txt` using the installed tool versions.

**Verification note:** The source was compile-checked and smoke-tested. Pylint, Bandit, and Flake8 could not be executed in the authoring environment because the packages were unavailable and package installation was blocked by network resolution. Do not treat a score or a clean report as verified until the commands above have been run locally.
