# LAB 5 — Static Code Analysis

**Student:** Dhanush Gowda A S  
**SRN:** PES1UG25CS812  
**Folder:** `LAB5_PES1UG25CS812`

## Lab problem

Retail Point of Sale & Discount Tracker — static analysis and remediation using Pylint, Bandit, and Flake8.

## Files

- `pos_system.py` — corrected POS implementation.
- `issues.md` — issue register, severity, description, and remediation.
- `reflection.md` — responses to four standard reflection areas.
- `tests/test_pos_system.py` — regression tests for core behavior and validation.
- `run_analysis.py` — helper to run the three analysis tools and save their outputs.
- `requirements.txt` — analysis tool dependencies.

## Setup and execution

```bash
python -m pip install -r requirements.txt
python pos_system.py
python -m unittest discover -s tests -v
python run_analysis.py
```

The helper creates `pylint_report.txt`, `bandit_report.txt`, and `flake8_report.txt` from the local tool versions. No static-analysis score is claimed until those commands have actually been executed.

## Handout note

The starter repository does not contain the separate lab handout. The reflection document therefore addresses four standard topics for this exercise; compare its headings with the exact prompts in your class handout before submission.

## Reference

Starter repository: https://github.com/SETAPESU26/L5_02_retail_pos
