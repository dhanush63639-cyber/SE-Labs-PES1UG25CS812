# LAB 5 — Static Code Analysis

**Student:** Dhanush Gowda A S  
**SRN:** PES1UG25CS812  
**Folder:** `LAB5_PES1UG25CS812`

## Lab problem

Retail Point of Sale & Discount Tracker — static analysis and remediation using Pylint, Bandit, and Flake8.

## Deliverable files

- `pos_system_before.py` — original vulnerable starter implementation used for the before analysis.
- `pos_system.py` — corrected POS implementation.
- `pylint_report_before.txt`, `pylint_report_after.txt` — Pylint outputs for both versions.
- `bandit_report_before.txt`, `bandit_report_after.txt` — Bandit outputs for both versions.
- `flake8_report_before.txt`, `flake8_report_after.txt` — Flake8 outputs for both versions.
- `issues.md` — issue register, severity, description, and remediation.
- `reflection.md` — responses to four standard reflection areas.
- `report.md` — consolidated lab report and reproducibility details.
- `tests/test_pos_system.py` — regression tests for core behavior and validation.
- `run_analysis.py` — generates all six before/after analyzer reports.
- `requirements.txt` — analysis tool dependencies.

## Setup and execution

```bash
python -m pip install -r requirements.txt
python pos_system.py
python -m unittest discover -s tests -v
python run_analysis.py
```

The analysis script creates the six before/after report files listed above. Commit those generated text files after running the script so the repository contains the actual tool output. Do not manually invent or edit analyzer scores.

## Handout note

The starter repository does not contain the separate lab handout PDF. Add the official PDF supplied by your instructor to this folder if your submission requires it. The reflection document addresses four standard topics; compare its headings with the exact prompts in your class handout before submission.

## Reference

Starter repository: https://github.com/SETAPESU26/L5_02_retail_pos
