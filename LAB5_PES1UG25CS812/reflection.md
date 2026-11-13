# Lab 5 — Reflection

**Student:** Dhanush Gowda A S  
**SRN:** PES1UG25CS812  
**Topic:** Static Code Analysis — Retail Point of Sale & Discount Tracker

## 1. What is the difference between a linter and a security scanner?

A linter primarily checks source-code quality, style, naming, formatting, common programming mistakes, and maintainability. In this lab, Pylint and Flake8 help identify issues such as unused imports, naming conventions, missing documentation, and suspicious code patterns. A security scanner focuses on weaknesses that could be exploited. Bandit checks Python code for risky constructs, including dynamic execution with `eval()`, unsafe subprocess usage, and other common security problems. Their goals overlap, but neither tool replaces code review or testing.

## 2. Which issue was the most serious, and why?

The most serious issue was using `eval()` to process a promo code taken from user input. It treated input as executable Python rather than as a limited discount instruction. A malicious input could therefore execute unintended commands with the permissions of the running program. I replaced this design with an allow-list of three explicit promo codes: `SAVE10`, `SAVE50`, and `CLEAR`. This preserves the discount use case without evaluating arbitrary expressions.

## 3. Did the tools find every problem? What did you discover manually?

No. Static-analysis tools can detect many suspicious patterns, but they cannot reliably infer every business-rule error. Manual inspection found that negative item quantities and invalid tax rates could create misleading totals, the stock-update function did not actually update stock, and the demonstration passed a string quantity. I added input validation and implemented a stock dictionary. This shows why tool output must be combined with manual reasoning and runtime tests.

## 4. What did you learn about static code analysis?

I learned that static analysis is most useful as an early feedback loop rather than as proof that a program is correct or secure. Pylint and Flake8 improve consistency and maintainability, while Bandit highlights security-sensitive patterns. Fixing warnings should not be done mechanically: the developer must understand the underlying behavior and ensure the correction does not break the application. I also learned to validate inputs, avoid unsafe dynamic execution, manage files with context managers, and write code that is easier to test.
