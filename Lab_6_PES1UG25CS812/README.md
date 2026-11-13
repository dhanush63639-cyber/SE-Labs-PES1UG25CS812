# Lab 6 — Code Coverage and Branch Coverage Analysis

**Course:** Software Engineering Test Automation (SETA)  
**Lab:** 6  
**Application:** Car Rental Rate and Fleet Telematics  
**Student:** Dhanush Gowda A S  
**USN:** PES1UG25CS812

## Folder contents

- `screenshots/` — location for genuine execution and coverage evidence.
- `car_rental_rate.py` — application module supplied for the lab.
- `test_car_rental.py` — basic functional test.
- `CodeCoverageTest_car_rental_rate.py` — statement/line coverage tests.
- `BranchCoverageTest_car_rental_rate.py` — branch and boundary coverage tests.
- `coverage_analysis_report.md` — measured coverage results and analysis.
- `requirements.txt` — Python test dependencies.
- `.coveragerc` — coverage configuration.
- `pytest.ini` — pytest discovery for the two coverage test filenames.
- `.gitignore` — generated-file exclusions.

## Setup

```bash
python -m pip install -r requirements.txt
```

## Run tests and coverage

```bash
pytest -v
coverage erase
coverage run --branch -m pytest -q
coverage report -m
coverage html
```

Open `htmlcov/index.html` to inspect line and branch details.

The current test run passed all 12 tests and measured 100% statement and branch coverage for the application module. See `coverage_analysis_report.md` for the breakdown. Regenerate coverage locally to reproduce the result.
