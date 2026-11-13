# Lab 7 — Fuzzing for Input Validation Bugs

**Student:** Dhanush Gowda A S  
**USN:** PES1UG25CS812  
**Project:** Car Rental Rate

This submission follows the six steps in the supplied Lab 7 student handout.

## Deliverables
- `processor.py` — hardened versions of all three application functions
- `test_processor.py` — Hypothesis fuzz tests and deterministic regression tests
- `requirements.txt` — pytest, Hypothesis and report-generation dependencies
- `LAB7_FuzzTesting_Report.pdf` — generated execution report with four terminal-output screenshots
- `screenshots/` — individual evidence images for Steps 2, 4, 5 and 6
- `evidence/before_fix/` — original buggy processor and the same tests to reproduce initial failures
- `generate_report.py` — regenerates the PDF and screenshots from actual command output

## Functions hardened
- `sanitize_license_plate`: rejects non-string, empty and invalid-character inputs; removes supported separators and uppercases valid plates.
- `parse_trip_mileage`: rejects wrong types, empty fields, non-numeric, negative, NaN and infinite mileage values.
- `format_rental_invoice`: validates the three-field record, non-empty driver/category, and positive integer rental days.

## Run locally
```bash
python -m pip install -r requirements.txt
python processor.py
python -m pytest -v test_processor.py
```

Hypothesis generates up to 150 examples per fuzz test. GitHub Actions runs the original buggy version first, verifies that the tests expose defects, runs the fixed version, reruns all tests, and commits the generated PDF and screenshot evidence.
