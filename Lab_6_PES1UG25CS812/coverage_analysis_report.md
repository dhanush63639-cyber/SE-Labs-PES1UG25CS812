# Lab 6 — Code Coverage and Branch Coverage Analysis

**Course:** Software Engineering Test Automation (SETA)  
**Application:** Car Rental Rate and Fleet Telematics  
**Student:** Dhanush Gowda A S  
**USN:** PES1UG25CS812

## Objective

Evaluate the supplied car-rental module using pytest and measure statement and branch coverage.

## Test execution

Command:

```bash
coverage erase
coverage run --branch -m pytest -q
coverage report -m
```

## Verified local result

The test suite was executed against the submitted `car_rental_rate.py` module and the three test files in this folder.

| Metric | Result |
|---|---:|
| Tests passed | 12 |
| Tests failed | 0 |
| Application statement coverage | 100% |
| Application branch coverage | 100% |
| Overall measured coverage | 100% |

The local coverage run reported 51 application statements and 36 branches, with 0 missed statements and 0 partial branches. Overall, 96 statements across the application and test files were measured, with 0 missed statements and 0 partial branches.

## Coverage scope

The test cases exercise input validation, confirmed/unconfirmed rentals, default values, vehicle-rate selection, rental duration, mileage boundaries, negative mileage, long-distance surcharges, underage drivers, audit thresholds, empty batches, and telematics speeding streaks.

## Reproduce the result

Install dependencies using `python -m pip install -r requirements.txt`, then run the commands above. Open `htmlcov/index.html` after `coverage html` to inspect the detailed report.

Coverage data is generated locally and is intentionally excluded from version control; regenerate it when reproducing the measurements.
