# Lab 7 — Test Execution Report

**Student:** Dhanush Gowda A S  
**USN:** PES1UG25CS812  
**Project:** L6_L7_02 — Car Rental Rate  
**Test framework:** pytest 9.2.0  
**Property-based testing:** Hypothesis 6.170.15  
**Runtime:** Python 3.12.16 (GitHub Actions, Ubuntu)

## Execution result

**PASS — 7 tests passed in 2.42 seconds.**

| Test | Result |
|---|---|
| Hypothesis: license plate accepts generated string inputs and handles None | PASS |
| Hypothesis: mileage parser handles generated strings and invalid input | PASS |
| Hypothesis: invoice formatter handles generated strings and malformed records | PASS |
| License plate removes supported delimiters and uppercases output | PASS |
| Mileage CSV values are converted to floats | PASS |
| SUV invoice uses $50/day | PASS |
| Non-SUV invoice uses $30/day | PASS |

Each Hypothesis test is configured for up to 200 generated examples, with the deadline disabled to avoid timing-related false failures.

## CI execution

- Workflow: `Lab 7 Hypothesis Tests`
- Trigger: push to `main`
- Run ID: `43407092113`
- Overall workflow: **success**
- Dependency installation: **success**
- Hypothesis test step: **success**

[View the GitHub Actions run](https://github.com/dhanush63639-cyber/SE-Labs-PES1UG25CS812/actions/runs/43407092113)

## Conclusion

The Lab 7 Hypothesis fuzz tests and deterministic regression tests executed successfully in the GitHub Actions environment. All seven collected tests passed. The test suite exercises valid and malformed inputs for the three supplied processor functions.
