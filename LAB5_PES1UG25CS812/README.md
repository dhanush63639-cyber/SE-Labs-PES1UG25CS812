# LAB 5 — Static Code Analysis

**Student:** Dhanush Gowda A S  
**SRN:** PES1UG25CS812  
**Folder:** `LAB5_PES1UG25CS812`

## Lab problem

Retail Point of Sale & Discount Tracker — static analysis and remediation using Pylint, Bandit, and Flake8.

## Files

- `pos_system.py` — corrected POS implementation.
- `issues.md` — issue register, severity, description, and remediation.
- `reflection.md` — responses to the four reflection questions.
- `run_analysis.py` — optional helper to run the three analysis tools and save their outputs.
- `requirements.txt` — analysis tool dependencies.

## Setup and execution

```bash
python -m pip install -r requirements.txt
python pos_system.py
python run_analysis.py
```

The helper creates `pylint_report.txt`, `bandit_report.txt`, and `flake8_report.txt`. These are generated from the local tool versions when the helper is run; no static-analysis score is claimed until those commands have actually been executed.

## Reference

Starter repository: https://github.com/SETAPESU26/L5_02_retail_pos
