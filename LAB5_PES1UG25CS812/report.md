# Lab 5 — Static Code Analysis Report

**Student:** Dhanush Gowda A S  
**SRN:** PES1UG25CS812  
**Project:** Retail Point of Sale & Discount Tracker

## Objective

Analyze the supplied Retail POS starter program with Pylint, Bandit, and Flake8, document defects, remediate the implementation, and compare the analyzer output before and after the changes.

## Baseline and remediation

The baseline is preserved in `pos_system_before.py`. The corrected implementation is `pos_system.py`. The issue register in `issues.md` maps the original defects to their fixes. Regression tests are in `tests/test_pos_system.py`.

## Reproducible analysis

Install the tools and run:

```bash
python -m pip install -r requirements.txt
python run_analysis.py
```

The script generates six real tool-output files:

- `pylint_report_before.txt`
- `pylint_report_after.txt`
- `bandit_report_before.txt`
- `bandit_report_after.txt`
- `flake8_report_before.txt`
- `flake8_report_after.txt`

These files are generated from the installed tool versions. Scores and findings must be taken from those outputs; this report does not invent scores or claim that a tool found zero issues without its report.

## Validation

Run the regression suite:

```bash
python -m unittest discover -s tests -v
```

Record the actual test result and the Pylint score from `pylint_report_after.txt` after execution.

## Deliverables

See `README.md` for setup instructions, `issues.md` for the issue register, and `reflection.md` for the reflection responses.
