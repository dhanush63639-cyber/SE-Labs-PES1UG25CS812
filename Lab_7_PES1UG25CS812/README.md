# Lab 7 — Fuzz Testing with Hypothesis

**Student:** Dhanush Gowda A S  
**USN:** PES1UG25CS812  
**Project:** L6_L7_02 — Car Rental Rate

## Objective

Apply property-based fuzz testing with Hypothesis to explore edge cases in three input-processing routines and detect parsing failures.

## Functions under test

- `sanitize_license_plate(plate)`: trims whitespace, removes hyphens, spaces, underscores and hash characters, and converts the result to uppercase.
- `parse_trip_mileage(mileage_csv)`: parses a comma-separated sequence of mileage values as floats.
- `format_rental_invoice(record)`: parses a `Driver:Days:Category` record and applies the SUV rate ($50/day) or standard rate ($30/day).

## Files

| File | Purpose |
|---|---|
| `processor.py` | Processor implementation supplied with the lab |
| `test_processor.py` | Hypothesis fuzz tests and deterministic regression tests |
| `requirements.txt` | Test dependencies |

## Setup and execution

Use Python 3.10 or later.

```bash
python -m venv .venv
```

Activate the environment, then install dependencies:

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -v
```

**Linux / macOS**
```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -v
```

Hypothesis generates up to 200 examples per fuzz test. The tests check valid results and expected exceptions for malformed inputs.

## Notes

The processor retains the starter lab's behavior so that the fuzz tests exercise the supplied routines rather than silently changing their input contract. The test suite treats invalid numeric CSV values and malformed rental records as expected parsing failures.
