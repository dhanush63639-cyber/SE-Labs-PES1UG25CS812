# Lab 6 — Code and Branch Coverage

**Student:** Dhanush Gowda A S  
**USN:** PES1UG25CS812  
**Module:** Car Rental Rate and Fleet Telematics

## Objective

Develop a pytest suite for the supplied car-rental pricing and fleet-telematics module and target 90–100% line and branch coverage.

## Files

- `car_rental_rate.py` — supplied application logic.
- `test_car_rental.py` — expanded pytest test suite.
- `requirements.txt` — test and coverage dependencies.

## Setup

Use Python 3.10 or later.

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run tests

```bash
pytest -v
```

## Measure line and branch coverage

```bash
coverage run --branch -m pytest
coverage report -m
coverage html
```

Open `htmlcov/index.html` to inspect line and branch execution details.

## Coverage strategy

The test suite covers invalid inputs, confirmed and unconfirmed rentals, defaults, each vehicle-rate branch, non-positive rental duration, mileage boundaries, negative and long trips, underage surcharges, risk-audit thresholds, empty batches, and telematics streak detection across multiple vehicles.

Coverage is measured from the executed test run. No percentage is claimed in advance; use the commands above to record the actual result in your lab submission.
